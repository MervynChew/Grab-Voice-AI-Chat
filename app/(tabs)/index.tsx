import React, { useState } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { Audio } from 'expo-av';
import axios from 'axios';
import { Platform } from 'react-native';  // Import Platform
import styles from './style'; // Ensure your style.js exists and is valid
import * as FileSystem from 'expo-file-system';

export default function App() {
  const [recording, setRecording] = useState(null);
  const [audioUri, setAudioUri] = useState(null);
  const [transcription, setTranscription] = useState(null);

  // Start recording
  const startRecording = async () => {
    try {
      const permission = await Audio.requestPermissionsAsync();
      if (permission.granted) {
        const { recording: newRecording } = await Audio.Recording.createAsync(
          Audio.RecordingOptionsPresets.HIGH_QUALITY
        );
        setRecording(newRecording);
      } else {
        console.error("Permission to record audio is required.");
      }
    } catch (err) {
      console.error("Error starting recording:", err);
    }
  };

  // Stop recording
  const stopRecording = async () => {
    try {
      if (recording) {
        await recording.stopAndUnloadAsync();
        const uri = recording.getURI();
        setAudioUri(uri);
        console.log("Recording stopped, audio URI:", uri);
      } else {
        console.log("No recording found to stop.");
      }
    } catch (err) {
      console.error("Error stopping recording:", err);
    }
  };

  // Function to detect MIME type (works for web and native)
  const getFileType = async (uri) => {
    if (Platform.OS === 'web') {
      // Web implementation using FileReader to detect MIME type
      const file = await fetch(uri).then(response => response.blob());
      const mimeType = file.type;
      return mimeType;
    } else {
      // Native implementation using expo-file-system
      const fileInfo = await FileSystem.getInfoAsync(uri);
      return fileInfo.mimeType || 'audio/wav'; // Default to 'audio/wav' if MIME type not found
    }
  };

  // Transcribe audio by sending it to FastAPI backend
  const transcribeAudio = async () => {
    if (!audioUri) return;

    try {
      // Get MIME type
      const mimeType = await getFileType(audioUri);

      // Dynamically set file extension based on MIME type
      const fileExtension = mimeType.includes('/') ? mimeType.split('/')[1] : 'wav';
      const fileName = 'audio.' + fileExtension;

      const formData = new FormData();
      
      // Check if the platform is web or native
      let file;
      if (Platform.OS === 'web') {
        const response = await fetch(audioUri);
        const blob = await response.blob();
        file = new File([blob], fileName, { type: mimeType });
      } else {
        // For native, use the uri directly
        file = {
          uri: audioUri,
          name: fileName,
          type: mimeType,
        };
      }

      formData.append('file', file);

      // Debugging the FormData
      console.log("Form Data:", formData);
      console.log("MIME Type:", mimeType);
      console.log("File Name:", fileName);
      console.log("Audio URI:", audioUri);

      const response = await axios.post('http://192.168.100.5:8000/transcribe', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const transcriptionText = response.data.transcription;
      setTranscription(transcriptionText);
      console.log("Transcription:", transcriptionText);
    } catch (err) {
      console.error("Error during transcription:", err);
      setTranscription("Error during transcription. Please try again.");
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Voice Transcription App</Text>
      <View style={styles.buttonsContainer}>
        <TouchableOpacity style={[styles.button, styles.startButton]} onPress={startRecording}>
          <Text style={styles.buttonText}>Start Recording</Text>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.button, styles.stopButton]} onPress={stopRecording}>
          <Text style={styles.buttonText}>Stop Recording</Text>
        </TouchableOpacity>
        {audioUri && (
          <TouchableOpacity style={[styles.button, styles.transcribeButton]} onPress={transcribeAudio}>
            <Text style={styles.buttonText}>Transcribe</Text>
          </TouchableOpacity>
        )}
      </View>
      {transcription && (
        <Text style={styles.transcriptionText}>Transcription: {transcription}</Text>
      )}
    </View>
  );
}

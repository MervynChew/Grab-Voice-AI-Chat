import React, { useState } from 'react';
import { Button, View, Text } from 'react-native';
import { Audio } from 'expo-av';
import axios from 'axios';

export default function App() {
  const [recording, setRecording] = useState();
  const [audioUri, setAudioUri] = useState(null);
  const [transcription, setTranscription] = useState(null);

  // Function to start recording
  const startRecording = async () => {
    try {
      const permission = await Audio.requestPermissionsAsync();
      if (permission.granted) {
        const { recording } = await Audio.Recording.createAsync(
          Audio.RecordingOptionsPresets.HIGH_QUALITY
        );
        setRecording(recording);
      } else {
        console.error("Permission to record audio is required.");
      }
    } catch (err) {
      console.error("Error starting recording:", err);
    }
  };

  // Function to stop recording
  const stopRecording = async () => {
    try {
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      setAudioUri(uri);
      console.log("Recording stopped, audio URI:", uri);
    } catch (err) {
      console.error("Error stopping recording:", err);
    }
  };

  // Function to send audio to Whisper for transcription
  const transcribeAudio = async () => {
    const formData = new FormData();
    formData.append('file', {
      uri: audioUri,
      name: 'audio.wav',
      type: 'audio/wav',
    });
    
    try {
      const response = await axios.post('YOUR_BACKEND_URL', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const transcriptionText = response.data.transcription;
      setTranscription(transcriptionText);
      console.log("Transcription:", transcriptionText);
    } catch (err) {
      console.error("Error during transcription:", err);
    }
  };

  return (
    <View>
      <Button title="Start Recording" onPress={startRecording} />
      <Button title="Stop Recording" onPress={stopRecording} />
      {audioUri && <Button title="Transcribe" onPress={transcribeAudio} />}
      {transcription && <Text>Transcription: {transcription}</Text>}
    </View>
  );
}

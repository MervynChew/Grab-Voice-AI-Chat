import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { Audio } from 'expo-av';
import axios from 'axios';
import { Platform } from 'react-native';  // Import Platform
import * as Speech from 'expo-speech'; // Import expo-speech
import styles from './style'; // Ensure your style.js exists and is valid
import * as FileSystem from 'expo-file-system';
import { Picker } from '@react-native-picker/picker'; // Import Picker

export default function App() {
  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  const [audioUri, setAudioUri] = useState<string | null>(null);
  const [transcription, setTranscription] = useState<string | null>(null);

  const [chatbotReply, setChatbotReply] = useState<string | null>(null);

  // States for voice selection
  const [availableVoices, setAvailableVoices] = useState<Speech.Voice[]>([]);
  const [selectedVoice, setSelectedVoice] = useState<string | null>(null);
  // States for language selection
  const [availableLanguages, setAvailableLanguages] = useState<string[]>([]);
  const [selectedLanguage, setSelectedLanguage] = useState<string | null>(null);

  // useEffect hook for fetching voices and languages
  useEffect(() => {
    async function loadSpeechData() {
      try {
        const voices = await Speech.getAvailableVoicesAsync();
        setAvailableVoices(voices);

        // Extract unique languages
        const languages = [...new Set(voices.map(v => v.language))].sort();
        setAvailableLanguages(languages);

        // Set default language (try common ones first, then fallback)
        const defaultLang = languages.find(l => l.startsWith('en')) || languages[0];
        if (defaultLang) {
            setSelectedLanguage(defaultLang);
        }
        
      } catch (error) {
        console.error("Error loading speech voices/languages:", error);
      }
    }
    loadSpeechData();
  }, []);

  // useEffect hook to set default voice based on selected language
  useEffect(() => {
    if (selectedLanguage && availableVoices.length > 0) {
        // Find voices for the selected language
        const voicesForLanguage = availableVoices.filter(v => v.language === selectedLanguage);
        
        // Try setting a default based on common identifiers, otherwise first available for the language
        const defaultVoice = voicesForLanguage.find(v => v.identifier.includes('Samantha') || v.identifier.includes('Default') || v.identifier.includes('Google')) || 
                           voicesForLanguage[0]; // Fallback to the first voice for the language

        if (defaultVoice) {
            setSelectedVoice(defaultVoice.identifier);
        } else {
            setSelectedVoice(null); // No voice found for this language
        }
    }
  }, [selectedLanguage, availableVoices]); // Rerun when language or voices change

  // Start recording
  const startRecording = async () => {
    try {
      Speech.stop(); // Stop any ongoing speech before starting recording
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
      Speech.stop(); // Stop any ongoing speech before stopping recording
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
  const getFileType = async (uri: string) => {
    if (Platform.OS === 'web') {
      // Web implementation using FileReader to detect MIME type
      const file = await fetch(uri).then(response => response.blob());
      const mimeType = file.type;
      return mimeType;
    } else {
      // Native implementation using expo-file-system
      const fileInfo = await FileSystem.getInfoAsync(uri);
      // Check for mimeType property directly
      return 'mimeType' in fileInfo && typeof fileInfo.mimeType === 'string' ? fileInfo.mimeType : 'audio/wav';
    }
  };

  // Function to speak the chatbot response
  const speakResponse = (text: string) => {
    Speech.speak(text, {
      language: 'en-US', // Base language setting
      voice: selectedVoice || undefined, // Use selected voice identifier
    });
  };

  // Transcribe audio by sending it to FastAPI backend
  const transcribeAudio = async () => {
    if (!audioUri) return;
  
    try {
      // Get MIME type
      const mimeType = await getFileType(audioUri);
  
      // Dynamically set file extension based on MIME type
      const fileExtension = mimeType.includes("/")
        ? mimeType.split("/")[1]
        : "wav";
      const fileName = "audio." + fileExtension;
  
      const formData = new FormData();
  
      // Check if the platform is web or native
      let file;
      if (Platform.OS === "web") {
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

      formData.append("file", file as any);

      // Debugging the FormData
      console.log("Form Data:", formData);
      console.log("MIME Type:", mimeType);
      console.log("File Name:", fileName);
      console.log("Audio URI:", audioUri);
  
      try {
        const response = await axios.post(
          "http://192.168.100.5:8000/transcribe",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
  
        console.log(response.data);  // This works because response is defined here
  
        // Only access response if the request was successful
        const transcriptionText = response.data.transcription;
        setTranscription(transcriptionText);
  
        // Now send that to chatbot
        await sendToChatbot(transcriptionText);
  
        console.log("Transcription:", transcriptionText);
      } catch (error) {
        console.error('Error during transcription:', error.response ? error.response.data : error.message);
        setTranscription("Error during transcription. Please try again.");
      }
  
    } catch (err) {
      console.error("Error during transcription:", err);
      setTranscription("Error during transcription. Please try again.");
    }
  };


  // Send transcription to chatbot backend and get a response
  const sendToChatbot = async (message: string) => {
    try {
      const response = await axios.post('http://10.213.6.220:8000/chat', {
        message: message,
      });
  
      const botReply = response.data.reply;
      console.log("Chatbot Reply:", botReply);
      setChatbotReply(botReply);
      speakResponse(botReply); // Speak the response
    } catch (error) {
      console.error("Error contacting chatbot:", error);
      setChatbotReply("Error contacting chatbot. Please try again.");
    }
  };
  


  return (
    <View style={styles.container}>
      <Text style={styles.header}>Voice Transcription App</Text>
      <View style={styles.buttonsContainer}>
        <TouchableOpacity
          style={[styles.button, styles.startButton]}
          onPress={startRecording}
        >
          <Text style={styles.buttonText}>Start Recording</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.button, styles.stopButton]}
          onPress={stopRecording}
        >
          <Text style={styles.buttonText}>Stop Recording</Text>
        </TouchableOpacity>
        {audioUri && (
          <TouchableOpacity
            style={[styles.button, styles.transcribeButton]}
            onPress={transcribeAudio}
          >
            <Text style={styles.buttonText}>Transcribe</Text>
          </TouchableOpacity>
        )}
      </View>

      {/* Language Selection Dropdown */} 
      {availableLanguages.length > 0 && (
        <View style={styles.pickerContainer}> 
          <Text style={styles.pickerLabel}>Select Language:</Text>
          <Picker
            selectedValue={selectedLanguage}
            style={styles.picker} 
            onValueChange={(itemValue) => setSelectedLanguage(itemValue)}
          >
            {availableLanguages.map((lang) => (
              <Picker.Item key={lang} label={lang} value={lang} /> // Display language code, consider mapping to full names if needed
            ))}
          </Picker>
        </View>
      )}

      {/* Voice Selection Dropdown - Filtered by Language */} 
      {availableVoices.length > 0 && selectedLanguage && (
        <View style={styles.pickerContainer}> 
          <Text style={styles.pickerLabel}>Select Voice:</Text>
          <Picker
            selectedValue={selectedVoice}
            style={styles.picker} 
            onValueChange={(itemValue) => setSelectedVoice(itemValue)}
            enabled={!!selectedVoice} // Disable if no voice is selected/available for the language
          >
            {availableVoices
              .filter(voice => voice.language === selectedLanguage) // Filter voices by selected language
              .map((voice) => (
                <Picker.Item key={voice.identifier} label={`${voice.name} (${voice.quality || 'default'})`} value={voice.identifier} />
            ))}
          </Picker>
        </View>
      )}

      {transcription && (
        <View style={styles.transcriptionContainer}>
          <Text style={styles.sectionHeader}>Transcription:</Text>
          <Text style={styles.transcriptionText}>{transcription}</Text>
          <Text style={styles.sectionHeader}>Chatbot Reply:</Text>
          <Text style={styles.chatbotText}>{chatbotReply}</Text>
          {/* Replay Button */} 
          <TouchableOpacity
            style={[styles.button, styles.replayButton]} // Add styles for replay button
            onPress={() => { if (chatbotReply) speakResponse(chatbotReply); }} // Check if chatbotReply is not null
          >
            <Text style={styles.buttonText}>Replay</Text>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
}

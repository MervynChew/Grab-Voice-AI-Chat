import React, { useState, useEffect, useRef } from 'react';
import { View, Text, TouchableOpacity, ScrollView, FlatList, StyleSheet } from 'react-native';
import { Audio } from 'expo-av';
import axios from 'axios';
import { Platform } from 'react-native';  // Import Platform
import * as Speech from 'expo-speech'; // Import expo-speech
import styles from './style'; // Ensure your style.js exists and is valid
import * as FileSystem from 'expo-file-system';
import { Picker } from '@react-native-picker/picker'; // Import Picker

// Define the structure for a chat message
interface ChatMessage {
  id: string;
  sender: 'user' | 'bot' | 'error';
  text: string;
}

export default function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  const [audioUri, setAudioUri] = useState<string | null>(null);

  // New state for chat history
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const flatListRef = useRef<FlatList>(null); // Ref for scrolling

  // States for voice selection
  const [availableVoices, setAvailableVoices] = useState<Speech.Voice[]>([]);
  const [selectedVoice, setSelectedVoice] = useState<string>(""); // Default to empty string

  // States for language selection
  const [availableLanguages, setAvailableLanguages] = useState<string[]>([]);
  const [selectedLanguage, setSelectedLanguage] = useState<string | null>(null);

  // New state for driver type
  const [driverType, setDriverType] = useState<'delivery' | 'ride'>('delivery'); // Default to delivery

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
            setSelectedVoice(""); // No voice found for this language
        }
    }
  }, [selectedLanguage, availableVoices]); // Rerun when language or voices change


  const handlePress = async () => {
    if (!isRecording) {
      setIsRecording(true);
      const rec = await startRecording(); // startRecording should return the object
  
    } else {
      await stopRecording(); // Make sure this function stops recording properly
      setIsRecording(false);
  
      // Ensure audioUri is set and then transcribe
      if (audioUri) {
        transcribeAudio();
      } else {
        // Handle case where audioUri is not ready yet (e.g., show an error message)
        console.log("Audio URI not available.");
      }
    }
  };

  // Function to add a message to the chat history
  const addMessageToHistory = (sender: 'user' | 'bot' | 'error', text: string) => {
    setChatHistory(prevHistory => [
      ...prevHistory,
      { id: Date.now().toString() + Math.random(), sender, text } // Basic unique ID
    ]);
  };

   // Scroll to the bottom whenever chat history updates
   useEffect(() => {
    if (flatListRef.current) {
      flatListRef.current.scrollToEnd({ animated: true });
    }
  }, [chatHistory]);

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
        return newRecording;  // Return the newRecording object
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
      const { sound, status } = await recording.stopAndUnloadAsync();
      const uri = recording.getURI(); // Retrieve the URI after stopping
      setAudioUri(uri);  // Update audioUri in the state
      return { sound, status };  // You can return the sound object if necessary
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
        addMessageToHistory('user', transcriptionText); // Add user message to history
  
        // Now send that to chatbot
        await sendToChatbot(transcriptionText);
  
        console.log("Transcription:", transcriptionText);
      } catch (error: any) {
        const errorMessage = "Error during transcription. Please try again.";
        console.error('Error during transcription:', error.response ? error.response.data : error.message);
        addMessageToHistory('error', errorMessage); // Add error message to history
      }
  
    } catch (err: any) {
      const errorMessage = "Error preparing transcription request.";
      console.error("Error during transcription setup:", err);
      addMessageToHistory('error', errorMessage); // Add error message to history
    }
  };


  // Send transcription to chatbot backend and get a response
  const sendToChatbot = async (message: string) => {
    try {
       // Include the selected driver type in the request
       // Also include the recent chat history (e.g., last 4 messages)
       const recentHistory = chatHistory.slice(-4);

      const response = await axios.post('http://192.168.100.5:8000/chat', {
        message: message,
        driver_type: driverType, // Add driver type here
        chat_history: recentHistory // Add recent history here
      });
  
      const botReply = response.data.reply;
      console.log("Chatbot Reply:", botReply);
      addMessageToHistory('bot', botReply); // Add bot message to history
      speakResponse(botReply); // Speak the response
    } catch (error: any) {
      const errorMessage = "Error contacting chatbot. Please try again.";
      console.error("Error contacting chatbot:", error.response ? error.response.data : error.message);
      addMessageToHistory('error', errorMessage); // Add error message to history
    }
  };
  
  // Function to replay the last bot message
  const replayLastBotMessage = () => {
    const lastBotMessage = [...chatHistory].reverse().find(msg => msg.sender === 'bot');
    if (lastBotMessage) {
        speakResponse(lastBotMessage.text);
    } else {
        console.log("No bot message found to replay.");
        // Optionally, provide user feedback like an alert
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Voice Chat App</Text>


      <View style={localStyles.layoutWrapper}>


        <View style={localStyles.controlsContainer}>
        <View style={localStyles.container}>
              <TouchableOpacity
                style={[
                  localStyles.circleButton,
                  isRecording ? localStyles.recording : localStyles.notRecording,
                ]}
                onPress={handlePress}
              >
                <Text style={localStyles.buttonText}>
                  {isRecording ? 'Stop & Transcribe' : 'Start'}
                </Text>
              </TouchableOpacity>
            </View>


            {availableLanguages.length > 0 && (
              <View style={styles.pickerContainer}>
                <Text style={styles.pickerLabel}>Language:</Text>
                <Picker
                  selectedValue={selectedLanguage}
                  style={styles.picker}
                  onValueChange={(itemValue) => setSelectedLanguage(itemValue)}
                >
                  {availableLanguages.map((lang) => (
                    <Picker.Item key={lang} label={lang} value={lang} />
                  ))}
                </Picker>
              </View>
            )}



            {availableVoices.length > 0 && selectedLanguage && (
              <View style={styles.pickerContainer}>
                <Text style={styles.pickerLabel}>Voice:</Text>
                <Picker
                  selectedValue={selectedVoice}
                  style={styles.picker}
                  onValueChange={(itemValue) => setSelectedVoice(itemValue)}
                  enabled={!!selectedVoice}
                >
                  {availableVoices
                    .filter(voice => voice.language === selectedLanguage)
                    .map((voice) => (
                      <Picker.Item key={voice.identifier} label={`${voice.name} (${voice.quality || 'default'})`} value={voice.identifier} />
                  ))}
                </Picker>
              </View>
            )}

             <TouchableOpacity
                  style={[styles.button, styles.replayButton, localStyles.replayButtonPosition]} // Add styles for replay button
                  onPress={replayLastBotMessage} // Use updated replay function
                  disabled={!chatHistory.some(msg => msg.sender === 'bot')} // Disable if no bot message exists
               >
                  <Text style={styles.buttonText}>Replay Last</Text>
             </TouchableOpacity>


             <View style={styles.pickerContainer}>
               <Text style={styles.pickerLabel}>Driver Type:</Text>
               <Picker
                 selectedValue={driverType}
                 style={styles.picker}
                 onValueChange={(itemValue) => setDriverType(itemValue)}
               >
                 <Picker.Item label="Delivery Driver" value="delivery" />
                 <Picker.Item label="Ride Driver (E-hailing)" value="ride" />
               </Picker>
             </View>
        </View>


    
        <View style={localStyles.chatContainer}>
           <FlatList
              ref={flatListRef}
              data={chatHistory}
              keyExtractor={(item) => item.id}
              renderItem={({ item }) => (
                <View style={[
                    localStyles.messageBubble,
                    item.sender === 'user' ? localStyles.userBubble : localStyles.botBubble,
                    item.sender === 'error' ? localStyles.errorBubble : null // Style for error messages
                ]}>
                    <Text style={localStyles.messageText}>{item.text}</Text>
                </View>
              )}
              ListEmptyComponent={<Text style={localStyles.emptyChatText}>No messages yet. Start recording!</Text>}
          />
        </View>

      </View> 

    </View>
  );
}

// Add some basic local styles for the chat UI
// These might need refinement and integration with your existing styles.js
const localStyles = StyleSheet.create({
  layoutWrapper: { // New style for the main horizontal layout
    flex: 1,
    flexDirection: 'row',
  },
  controlsContainer: {
    width: 280, // Assign a fixed width for the controls column
    padding: 10, // Add padding around controls
    borderRightWidth: 1, // Add a separator line
    borderRightColor: '#ccc',
  },
  chatContainer: {
    flex: 1, // Takes remaining horizontal space
    padding: 10, // Add padding inside the chat area
  },
  messageBubble: {
    padding: 10,
    borderRadius: 15,
    marginBottom: 10,
    maxWidth: '80%',
  },
  userBubble: {
    backgroundColor: '#DCF8C6', // Light green for user
    alignSelf: 'flex-end',
    borderBottomRightRadius: 0,
  },
  botBubble: {
    backgroundColor: '#EAEAEA', // Light grey for bot
    alignSelf: 'flex-start',
    borderBottomLeftRadius: 0,
  },
  errorBubble: {
    backgroundColor: '#FFDEDE', // Light red for errors
    alignSelf: 'center',
    maxWidth: '90%',
  },
  messageText: {
    fontSize: 16,
  },
  emptyChatText: {
    textAlign: 'center',
    marginTop: 20,
    color: '#888',
  },
   replayButtonPosition: {
    marginTop: 10, // Add some space above the replay button
  },
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff', // Make sure container is visible
  },
  circleButton: {
    width: 100,
    height: 100,
    borderRadius: 50,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 5, // Android shadow
    shadowColor: '#000', // iOS shadow
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 3,
  },
  recording: {
    backgroundColor: '#ff4d4d', // red
  },
  notRecording: {
    backgroundColor: '#4caf50', // green
  },
  buttonText: {
    color: '#fff',
    fontWeight: 'bold',
    textAlign: 'center',
  },
});

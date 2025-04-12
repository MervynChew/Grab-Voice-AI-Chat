// styles.js
import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f7f7f7',
    padding: 20,
  },
  header: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 20,
  },
  buttonsContainer: {
    flexDirection: 'column',
    justifyContent: 'space-around',
    width: '100%',
    marginBottom: 20,
  },
  button: {
    padding: 15,
    marginVertical: 10,
    borderRadius: 5,
    alignItems: 'center',
  },
  startButton: {
    backgroundColor: '#4CAF50',
  },
  stopButton: {
    backgroundColor: '#F44336',
  },
  transcribeButton: {
    backgroundColor: '#2196F3',
  },
  buttonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
  },
  transcriptionText: {
    marginTop: 20,
    fontSize: 18,
    color: '#333',
    fontWeight: '500',
    textAlign: 'center',
  },


// Below Chatbot


  transcriptionContainer: {
    marginTop: 20,
  },
  
  chatbotContainer: {
    marginTop: 20,
    backgroundColor: '#f0f0f0',
    padding: 10,
    borderRadius: 10,
  },
  
  sectionHeader: {
    fontWeight: 'bold',
    fontSize: 16,
    marginBottom: 5,
  },
  
  transcriptionText: {
    fontSize: 15,
    color: '#333',
  },
  
  chatbotText: {
    fontSize: 15,
    color: '#007AFF',
  },
  pickerContainer: {
    marginTop: 20,
    width: '80%', // Adjust width as needed
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
  },
  pickerLabel: {
    fontSize: 16,
    color: '#555',
    paddingLeft: 10,
    paddingTop: 5,
  },
  picker: {
    height: 50,
    width: '100%',
  },
  replayButton: {
    backgroundColor: '#FFC107', // Example: Amber color
    paddingVertical: 8,       // Smaller padding
    paddingHorizontal: 15,
    marginTop: 10,            // Add some space above
    alignSelf: 'flex-start',  // Align to the left within its container
  },
  
});

export default styles;

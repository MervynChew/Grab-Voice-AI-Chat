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
  
});

export default styles;

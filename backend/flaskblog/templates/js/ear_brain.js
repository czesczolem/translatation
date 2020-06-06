<script>

    window.SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
    let finalTranscript = '';
    let recognition = new window.SpeechRecognition();
    recognition.interimResults = true;
    recognition.maxAlternatives = 10;
    recognition.continuous = true;
    recognition.lang = 'en-EN';
    recognition.onresult = (event) => {
      let interimTranscript = '';
      for (let i = event.resultIndex, len = event.results.length; i < len; i++) {
        let transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript;
        } else {
          interimTranscript += transcript;
        }
      }
      document.querySelector('#main-input').innerHTML = '<h1>' + finalTranscript + '<i style="color:#ddd;">' + interimTranscript + '</></h1>';
      if (finalTranscript) {
            postData('http://127.0.0.1:5000/brain_test', { answer: finalTranscript}).then((data) => {
            document.querySelector('#bot-output-1').innerHTML = '<h1>' + data.text + '</h1>'; // JSON data parsed by `response.json()` call
            finalTranscript = "";
      });
    }

    }
    recognition.start();
    recognition.onend = (event) => {
        recognition.start();
    };
</script>
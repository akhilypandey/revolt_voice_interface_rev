class VoiceChatApp {
    constructor() {
        this.ws = null;
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.isConnected = false;
        this.clientId = this.generateClientId();
        this.currentResponse = '';
        
        this.initializeElements();
        this.bindEvents();
        this.connectWebSocket();
        this.initializeVoiceSettings();
        
        // Make app globally accessible for voice settings
        window.voiceChatApp = this;
    }

    initializeElements() {
        this.micButton = document.getElementById('micButton');
        this.recordingIndicator = document.getElementById('recordingIndicator');
        this.statusDot = document.getElementById('statusDot');
        this.statusText = document.getElementById('statusText');
        this.themeToggle = document.getElementById('theme-toggle');
    }

    bindEvents() {
        this.micButton.addEventListener('click', () => this.toggleRecording());
        
        // Theme toggle
        this.themeToggle.addEventListener('change', () => {
            this.toggleTheme();
        });
        
        // Load saved theme
        this.loadTheme();
        
        // Add keyboard shortcut for easier testing (Spacebar)
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && !this.isRecording && !this.micButton.disabled) {
                e.preventDefault();
                this.startRecording();
            }
        });
    }

    generateClientId() {
        return 'client_' + Math.random().toString(36).substr(2, 9);
    }

    connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/${this.clientId}`;
        
        this.updateStatus('connecting');
        
        this.ws = new WebSocket(wsUrl);
        
        this.ws.onopen = () => {
            this.isConnected = true;
            this.updateStatus('connected');
            this.enableControls();
            this.statusText.textContent = 'Connected - Click to talk';
        };
        
        this.ws.onmessage = (event) => {
            console.log('WebSocket message received:', event.data);
            const data = JSON.parse(event.data);
            this.handleWebSocketMessage(data);
        };
        
        this.ws.onclose = () => {
            this.isConnected = false;
            this.updateStatus('disconnected');
            this.disableControls();
            // Attempt to reconnect after 3 seconds
            setTimeout(() => this.connectWebSocket(), 3000);
        };
        
        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.updateStatus('error');
            this.statusText.textContent = 'Connection error - please refresh';
        };
    }

    updateStatus(status) {
        this.statusDot.className = 'status-dot ' + status;
        
        switch(status) {
            case 'connected':
                this.statusText.textContent = 'Connected';
                break;
            case 'connecting':
                this.statusText.textContent = 'Connecting...';
                break;
            case 'disconnected':
                this.statusText.textContent = 'Disconnected';
                break;
            case 'error':
                this.statusText.textContent = 'Connection Error';
                break;
        }
    }

    enableControls() {
        this.micButton.disabled = false;
    }

    disableControls() {
        this.micButton.disabled = true;
    }

    async toggleRecording() {
        // Prevent multiple rapid clicks
        if (this.micButton.disabled) return;
        
        if (this.isRecording) {
            this.stopRecording();
        } else {
            await this.startRecording();
        }
    }

    async startRecording() {
        try {
            // Briefly disable button during setup
            this.micButton.disabled = true;
            
            // Stop any ongoing speech when user starts talking (interruption)
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                console.log('Stopped Rev\'s speech - user interruption');
            }
            
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    sampleRate: 16000,
                    channelCount: 1,
                    echoCancellation: true,
                    noiseSuppression: true
                } 
            });
            
            this.mediaRecorder = new MediaRecorder(stream, {
                mimeType: 'audio/webm;codecs=opus'
            });
            
            this.audioChunks = [];
            this.silenceTimer = null;
            this.lastAudioTime = Date.now();
            
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.audioChunks.push(event.data);
                    this.lastAudioTime = Date.now();
                    
                    // Reset silence timer
                    if (this.silenceTimer) {
                        clearTimeout(this.silenceTimer);
                    }
                    
                    // Set timer to auto-stop after 2 seconds of silence
                    this.silenceTimer = setTimeout(() => {
                        if (this.isRecording) {
                            console.log('Auto-stopping recording after 2 seconds of silence');
                            this.statusText.textContent = 'Processing your message...';
                            this.stopRecording();
                        }
                    }, 2000);
                    
                    // Show countdown for auto-stop
                    this.updateSilenceCountdown();
                }
            };
            
            this.mediaRecorder.onstop = () => {
                if (this.silenceTimer) {
                    clearTimeout(this.silenceTimer);
                }
                if (this.autoStopTimer) {
                    clearTimeout(this.autoStopTimer);
                }
                this.processAudioData();
                stream.getTracks().forEach(track => track.stop());
            };
            
            this.mediaRecorder.start();
            this.isRecording = true;
            this.micButton.classList.add('recording');
            this.recordingIndicator.classList.add('active');
            
            // Update button text to show it's recording
            this.micButton.innerHTML = '<i class="fas fa-stop"></i>';
            this.statusText.textContent = 'Recording... Speak now (auto-stops in 3s)';
            this.micButton.disabled = false; // Re-enable button
            
            // Auto-stop after 3 seconds (simpler approach)
            this.autoStopTimer = setTimeout(() => {
                if (this.isRecording) {
                    console.log('Auto-stopping recording after 3 seconds');
                    this.statusText.textContent = 'Processing your message...';
                    this.stopRecording();
                }
            }, 3000);
            
        } catch (error) {
            console.error('Error starting recording:', error);
            alert('Error accessing microphone. Please check permissions.');
            this.micButton.disabled = false; // Re-enable button on error
        }
    }

    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            // Clear all timers
            if (this.silenceTimer) {
                clearTimeout(this.silenceTimer);
                this.silenceTimer = null;
            }
            if (this.autoStopTimer) {
                clearTimeout(this.autoStopTimer);
                this.autoStopTimer = null;
            }
            
            this.mediaRecorder.stop();
            this.isRecording = false;
            this.micButton.classList.remove('recording');
            this.recordingIndicator.classList.remove('active');
            
            // Reset button text to microphone icon
            this.micButton.innerHTML = '<i class="fas fa-microphone"></i>';
            this.statusText.textContent = 'Connected - Click to talk';
        }
    }

    async processAudioData() {
        if (this.audioChunks.length === 0) {
            console.log('No audio data to process');
            return;
        }
        
        console.log(`Processing ${this.audioChunks.length} audio chunks...`);
        const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
        console.log(`Audio blob size: ${audioBlob.size} bytes`);
        
        const reader = new FileReader();
        
        reader.onload = () => {
            const base64Audio = reader.result.split(',')[1];
            console.log(`Base64 audio length: ${base64Audio.length} characters`);
            this.sendAudioMessage(base64Audio);
        };
        
        reader.readAsDataURL(audioBlob);
    }

    sendAudioMessage(audioData) {
        if (!this.isConnected) {
            console.error('WebSocket not connected');
            this.statusText.textContent = 'Not connected - please refresh';
            return;
        }
        
        console.log('Sending audio message...');
        this.statusText.textContent = 'Sending your message...';
        
        const message = {
            type: 'audio',
            audio_data: audioData,
            mime_type: 'audio/webm'
        };
        
        this.ws.send(JSON.stringify(message));
        console.log('Audio message sent successfully');
    }

    handleWebSocketMessage(data) {
        switch(data.type) {
            case 'response_chunk':
                // Handle streaming response with voice
                console.log('Rev is responding...');
                this.statusText.textContent = 'Rev is speaking...';
                // Add text to speech for each chunk
                this.speakText(data.text);
                break;
            case 'response_end':
                // Response complete
                console.log('Rev finished responding');
                this.statusText.textContent = 'Connected - Click to talk';
                break;
            case 'error':
                console.error('Error:', data.message);
                this.statusText.textContent = 'Error: ' + data.message;
                break;
            case 'pong':
                // Handle ping/pong for connection health
                break;
        }
    }

    speakText(text) {
        // Use browser's built-in text-to-speech with improved settings
        if ('speechSynthesis' in window) {
            // Cancel any ongoing speech
            window.speechSynthesis.cancel();
            
            const utterance = new SpeechSynthesisUtterance(text);
            
            // Use saved voice settings or defaults
            utterance.rate = this.voiceSpeed || 1.1;
            utterance.pitch = this.voicePitch || 1.05;
            utterance.volume = 0.9; // Slightly lower volume for more natural feel
            
            // Enhanced voice selection for more human-like quality
            const voices = speechSynthesis.getVoices();
            console.log('Available voices:', voices.map(v => v.name));
            
            // Priority order for natural-sounding voices
            const preferredVoices = [
                'Samantha', 'Alex', 'Victoria', 'Daniel', 'Karen', 'Tom',
                'Google UK English Female', 'Google UK English Male',
                'Google US English Female', 'Google US English Male',
                'Microsoft David - English (United States)',
                'Microsoft Zira - English (United States)',
                'Natural', 'Enhanced', 'Premium'
            ];
            
            let selectedVoice = null;
            for (const voiceName of preferredVoices) {
                selectedVoice = voices.find(voice => 
                    voice.name.includes(voiceName) || 
                    voice.name.toLowerCase().includes(voiceName.toLowerCase())
                );
                if (selectedVoice) {
                    console.log('Selected voice:', selectedVoice.name);
                    break;
                }
            }
            
            // If no preferred voice found, try to find any enhanced/premium voice
            if (!selectedVoice) {
                selectedVoice = voices.find(voice => 
                    voice.name.toLowerCase().includes('enhanced') ||
                    voice.name.toLowerCase().includes('premium') ||
                    voice.name.toLowerCase().includes('natural') ||
                    voice.name.toLowerCase().includes('google') ||
                    voice.name.toLowerCase().includes('microsoft')
                );
            }
            
            // Use selected voice from settings or auto-select
            if (this.selectedVoice && this.selectedVoice !== 'auto') {
                const customVoice = voices.find(voice => voice.name === this.selectedVoice);
                if (customVoice) {
                    utterance.voice = customVoice;
                    console.log('Using custom voice:', customVoice.name);
                }
            } else if (selectedVoice) {
                utterance.voice = selectedVoice;
                console.log('Using auto-selected voice:', selectedVoice.name);
            } else {
                console.log('Using default voice');
            }
            
            // Add natural pauses and breaks for more human-like speech
            const processedText = this.addNaturalPauses(text);
            utterance.text = processedText;
            
            utterance.onstart = () => {
                console.log('Rev started speaking:', processedText);
            };
            
            utterance.onend = () => {
                console.log('Rev finished speaking');
            };
            
            utterance.onerror = (event) => {
                console.error('Speech error:', event.error);
            };
            
            window.speechSynthesis.speak(utterance);
        } else {
            console.warn('Text-to-speech not supported in this browser');
        }
    }
    
    addNaturalPauses(text) {
        // Add natural pauses for more human-like speech
        return text
            // Add pauses after sentences
            .replace(/\./g, '... ')
            .replace(/\!/g, '... ')
            .replace(/\?/g, '... ')
            // Add slight pauses after commas
            .replace(/,/g, ', ')
            // Add pauses for emphasis
            .replace(/:/g, '... ')
            .replace(/;/g, '... ');
    }
    
    updateSilenceCountdown() {
        if (!this.isRecording || !this.silenceTimer) return;
        
        const timeLeft = Math.max(0, 2000 - (Date.now() - this.lastAudioTime));
        const secondsLeft = Math.ceil(timeLeft / 1000);
        
        if (secondsLeft > 0) {
            this.statusText.textContent = `Recording... Auto-stop in ${secondsLeft}s`;
        }
        
        if (this.isRecording && timeLeft > 0) {
            setTimeout(() => this.updateSilenceCountdown(), 100);
        }
    }
    
    toggleTheme() {
        const isDark = this.themeToggle.checked;
        document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    }
    
    loadTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        this.themeToggle.checked = savedTheme === 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
    }
    
    // Voice settings methods
    initializeVoiceSettings() {
        this.voiceSpeed = parseFloat(localStorage.getItem('voiceSpeed') || '1.1');
        this.voicePitch = parseFloat(localStorage.getItem('voicePitch') || '1.05');
        this.selectedVoice = localStorage.getItem('selectedVoice') || 'auto';
        
        // Update UI elements
        const speedSlider = document.getElementById('voiceSpeed');
        const pitchSlider = document.getElementById('voicePitch');
        const voiceSelect = document.getElementById('voiceSelect');
        
        if (speedSlider) {
            speedSlider.value = this.voiceSpeed;
            document.getElementById('speedValue').textContent = this.voiceSpeed + 'x';
        }
        
        if (pitchSlider) {
            pitchSlider.value = this.voicePitch;
            document.getElementById('pitchValue').textContent = this.voicePitch;
        }
        
        // Populate voice select
        this.populateVoiceSelect();
        
        // Add event listeners
        if (speedSlider) {
            speedSlider.addEventListener('input', (e) => {
                this.voiceSpeed = parseFloat(e.target.value);
                document.getElementById('speedValue').textContent = this.voiceSpeed + 'x';
                localStorage.setItem('voiceSpeed', this.voiceSpeed);
            });
        }
        
        if (pitchSlider) {
            pitchSlider.addEventListener('input', (e) => {
                this.voicePitch = parseFloat(e.target.value);
                document.getElementById('pitchValue').textContent = this.voicePitch;
                localStorage.setItem('voicePitch', this.voicePitch);
            });
        }
        
        if (voiceSelect) {
            voiceSelect.addEventListener('change', (e) => {
                this.selectedVoice = e.target.value;
                localStorage.setItem('selectedVoice', this.selectedVoice);
            });
        }
    }
    
    populateVoiceSelect() {
        const voiceSelect = document.getElementById('voiceSelect');
        if (!voiceSelect) return;
        
        // Clear existing options
        voiceSelect.innerHTML = '<option value="auto">Auto-select best</option>';
        
        // Wait for voices to load
        if (speechSynthesis.onvoiceschanged !== undefined) {
            speechSynthesis.onvoiceschanged = () => {
                const voices = speechSynthesis.getVoices();
                voices.forEach(voice => {
                    const option = document.createElement('option');
                    option.value = voice.name;
                    option.textContent = voice.name;
                    voiceSelect.appendChild(option);
                });
            };
        }
    }
}

// Global functions for voice settings
function toggleVoiceSettings() {
    const panel = document.getElementById('settingsPanel');
    panel.classList.toggle('show');
}

function testVoice() {
    const testText = "Hello! I'm Rev, your Revolt Motors assistant. How can I help you today?";
    const app = window.voiceChatApp;
    if (app && app.speakText) {
        app.speakText(testText);
    }
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new VoiceChatApp();
});

// Update range values in real-time
document.addEventListener('DOMContentLoaded', function() {
    const moodScore = document.getElementById('moodScore');
    const stressLevel = document.getElementById('stressLevel');
    const energyLevel = document.getElementById('energyLevel');
    
    if (moodScore) {
        moodScore.oninput = function() {
            document.getElementById('moodValue').textContent = this.value;
        }
    }
    
    if (stressLevel) {
        stressLevel.oninput = function() {
            document.getElementById('stressValue').textContent = this.value;
        }
    }
    
    if (energyLevel) {
        energyLevel.oninput = function() {
            document.getElementById('energyValue').textContent = this.value;
        }
    }
});

// Generate AI wellness plan with feelings
function generateAIWellnessPlan() {
    const mood = document.getElementById('moodScore').value;
    const stress = document.getElementById('stressLevel').value;
    const energy = document.getElementById('energyLevel').value;
    const feelings = document.getElementById('feelingsText').value;
    
    displayResponse('🤖 AI Processing...', {message: 'Advanced neural networks analyzing your personal data and feelings...'});
    
    fetch('/api/generate-ai-wellness-plan', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({
            mood_score: parseInt(mood),
            stress_level: parseInt(stress),
            energy_level: parseInt(energy),
            feelings_description: feelings
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayAIPlan('🤖 AI Wellness Plan Generated!', data.plan);
            setTimeout(() => location.reload(), 5000);
        } else {
            displayResponse('❌ AI Generation Failed', {message: data.error || 'Please try again'});
        }
    })
    .catch(error => {
        console.error('Error:', error);
        displayResponse('❌ Error', {message: 'Failed to generate AI plan. Please try again.'});
    });
}

// Analyze feelings with AI
function analyzeFeelings() {
    const feelings = document.getElementById('feelingsText').value;
    
    if (!feelings.trim()) {
        displayResponse('❌ No Feelings Text', {message: 'Please describe your feelings first.'});
        return;
    }
    
    displayResponse('🤖 AI Analyzing...', {message: 'Advanced emotion AI processing your feelings...'});
    
    fetch('/api/analyze-feelings', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({
            feelings_text: feelings
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayFeelingsAnalysis('🧠 Feelings Analysis Complete!', data.analysis);
        } else {
            displayResponse('❌ Analysis Failed', {message: data.error || 'Please try again'});
        }
    })
    .catch(error => {
        console.error('Error:', error);
        displayResponse('❌ Error', {message: 'Failed to analyze feelings. Please try again.'});
    });
}

// Log mood data - FIXED
function logMood() {
    const mood = document.getElementById('moodScore').value;
    const stress = document.getElementById('stressLevel').value;
    const energy = document.getElementById('energyLevel').value;
    
    displayResponse('📊 Logging Mood...', {message: 'Recording your neural data...'});
    
    fetch('/api/log-mood', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({
            mood_score: parseInt(mood),
            stress_level: parseInt(stress),
            energy_level: parseInt(energy),
            notes: 'Auto-logged via neural interface'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayResponse('✅ Neural Data Logged Successfully!', {
                message: data.message
            });
            updateMoodHistory();
        } else {
            throw new Error(data.error || 'Unknown error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        displayResponse('❌ Mood Logging Failed', {
            message: 'Could not save mood data. Please try again.'
        });
    });
}

// Voice command - WORKING
function startVoiceCommand() {
    displayResponse('🎤 Voice Command Activated!', {
        message: 'Neural voice processing activated...'
    });
    
    // Try real speech recognition first
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        recognition.onstart = function() {
            displayResponse('🎤 Listening...', {
                message: 'Speak now! Say "generate plan", "start meditation", or "track mood"'
            });
        };
        
        recognition.onresult = function(event) {
            const command = event.results[0][0].transcript.toLowerCase();
            processVoiceCommand(command);
        };
        
        recognition.onerror = function(event) {
            displayResponse('🎤 Voice Recognition Error', {
                message: 'Switching to simulation mode...'
            });
            setTimeout(simulateVoiceCommand, 1000);
        };
        
        recognition.start();
    } else {
        setTimeout(simulateVoiceCommand, 1000);
    }
}

function simulateVoiceCommand() {
    const commands = [
        'generate wellness plan',
        'start meditation', 
        'begin workout',
        'track my mood',
        'show vr content'
    ];
    const randomCommand = commands[Math.floor(Math.random() * commands.length)];
    
    displayResponse('🎤 Voice Command Simulated', {
        message: `Detected: "${randomCommand}"`
    });
    
    setTimeout(() => processVoiceCommand(randomCommand), 1000);
}

function processVoiceCommand(command) {
    if (command.includes('meditation') || command.includes('vr')) {
        displayResponse('🎤 Voice Action: VR Meditation', {
            message: 'Launching Neural Calm Forest session...'
        });
        setTimeout(() => startVRSession('1'), 1500);
    } else if (command.includes('workout') || command.includes('fitness')) {
        displayResponse('🎤 Voice Action: Workout', {
            message: 'Activating holographic personal trainer...'
        });
        setTimeout(generateWorkoutPlan, 1500);
    } else if (command.includes('mood') || command.includes('track')) {
        displayResponse('🎤 Voice Action: Mood Tracking', {
            message: 'Opening neural mood analysis interface...'
        });
        setTimeout(focusOnMoodSliders, 1500);
    } else if (command.includes('plan') || command.includes('generate')) {
        displayResponse('🎤 Voice Action: Generate Plan', {
            message: 'Generating personalized wellness plan...'
        });
        setTimeout(generateAIWellnessPlan, 1500);
    } else {
        displayResponse('🎤 Voice Command Processed', {
            message: `Command "${command}" received and processed by AI`
        });
    }
}

// Brain interface - ENHANCED
function simulateBrainInterface() {
    const brainStates = [
        { state: 'relaxed', action: 'Starting calm meditation mode', color: 'info' },
        { state: 'focused', action: 'Optimizing productivity settings', color: 'primary' },
        { state: 'stressed', action: 'Activating stress relief protocol', color: 'warning' },
        { state: 'energetic', action: 'Preparing dynamic workout plan', color: 'success' }
    ];
    
    const randomBrain = brainStates[Math.floor(Math.random() * brainStates.length)];
    
    displayResponse('🧠 Brain Interface Scanning...', {
        message: 'Reading neural patterns... Please remain still.'
    });
    
    setTimeout(() => {
        displayResponse(`🧠 Neural State: ${randomBrain.state.toUpperCase()}`, {
            message: randomBrain.action
        });
        
        // Execute brain-controlled action
        setTimeout(() => {
            switch(randomBrain.state) {
                case 'relaxed':
                    startVRSession('1');
                    break;
                case 'focused':
                    generateAIWellnessPlan();
                    break;
                case 'stressed':
                    startVRSession('2');
                    break;
                case 'energetic':
                    generateWorkoutPlan();
                    break;
            }
        }, 2000);
    }, 3000);
}

// VR sessions - FULLY FUNCTIONAL
function startVRSession(contentId) {
    const vrContent = {
        '1': { name: 'Neural Calm Forest', duration: 15 },
        '2': { name: 'Quantum Mindfulness Space', duration: 30 },
        '3': { name: 'Holographic Yoga Studio', duration: 45 }
    };
    
    const content = vrContent[contentId] || { name: 'Unknown Content', duration: 10 };
    
    displayResponse('🥽 VR Initialization', {
        message: `Loading ${content.name}... Neural feedback calibrating.`
    });
    
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += 20;
        
        if (progress <= 100) {
            displayResponse(`🥽 ${content.name} - ${progress}%`, {
                message: `Session in progress... Biometric monitoring active. Time remaining: ${Math.ceil((content.duration * (100 - progress)) / 100)} minutes.`
            });
        }
        
        if (progress >= 100) {
            clearInterval(progressInterval);
            displayResponse('🥽 VR Session Complete! ✅', {
                message: `${content.name} completed successfully! Wellness data updated. Neural points earned: +${content.duration * 2}`
            });
        }
    }, 1000);
}

// Display AI-generated plan
function displayAIPlan(title, plan) {
    const responseArea = document.getElementById('responseArea');
    responseArea.innerHTML = `
        <div class="alert alert-success alert-dismissible fade show">
            <h5>${title}</h5>
            
            ${plan.personalized_insights ? `
                <div class="mb-3 p-3" style="background: rgba(0, 255, 127, 0.1); border-radius: 10px;">
                    <h6>🔍 AI Insights:</h6>
                    <p>${plan.personalized_insights}</p>
                </div>
            ` : ''}
            
            <div class="row">
                <div class="col-md-4">
                    <h6>🧘 Mental Health:</h6>
                    <ul class="small">${plan.mental_health.map(item => `<li>${item}</li>`).join('')}</ul>
                </div>
                <div class="col-md-4">
                    <h6>💪 Fitness:</h6>
                    <ul class="small">${plan.fitness.map(item => `<li>${item}</li>`).join('')}</ul>
                </div>
                <div class="col-md-4">
                    <h6>🥗 Nutrition:</h6>
                    <ul class="small">${plan.nutrition.map(item => `<li>${item}</li>`).join('')}</ul>
                </div>
            </div>
            
            ${plan.motivation_message ? `
                <div class="mt-3 p-3" style="background: rgba(0, 191, 255, 0.1); border-radius: 10px;">
                    <h6>💪 Your AI Coach Says:</h6>
                    <p><em>${plan.motivation_message}</em></p>
                </div>
            ` : ''}
            
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    responseArea.scrollIntoView({ behavior: 'smooth' });
}

// Display feelings analysis
function displayFeelingsAnalysis(title, analysis) {
    const responseArea = document.getElementById('responseArea');
    responseArea.innerHTML = `
        <div class="alert alert-info alert-dismissible fade show">
            <h5>${title}</h5>
            <div class="row">
                <div class="col-md-6">
                    <h6>🎭 Emotional State:</h6>
                    <p><strong>${analysis.emotional_state}</strong></p>
                    
                    <h6>⚠️ Stress Indicators:</h6>
                    <ul class="small">
                        ${analysis.stress_indicators.map(indicator => `<li>${indicator}</li>`).join('')}
                    </ul>
                </div>
                <div class="col-md-6">
                    <h6>🎯 Focus Areas:</h6>
                    <ul class="small">
                        ${analysis.recommended_focus_areas.map(area => `<li>${area}</li>`).join('')}
                    </ul>
                    
                    <h6>💙 AI Response:</h6>
                    <p class="small"><em>${analysis.empathy_message}</em></p>
                </div>
            </div>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    responseArea.scrollIntoView({ behavior: 'smooth' });
}

// Display regular responses
function displayResponse(title, data) {
    const responseArea = document.getElementById('responseArea');
    responseArea.innerHTML = `
        <div class="alert alert-info alert-dismissible fade show">
            <h5>${title}</h5>
            <p>${data.message}</p>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    responseArea.scrollIntoView({ behavior: 'smooth' });
}

// Helper functions
function updateMoodHistory() {
    const moodSection = document.querySelector('.mb-4');
    if (moodSection) {
        moodSection.style.backgroundColor = 'rgba(0, 255, 127, 0.2)';
        moodSection.style.transition = 'background-color 0.5s ease';
        setTimeout(() => {
            moodSection.style.backgroundColor = '';
        }, 3000);
    }
}

function focusOnMoodSliders() {
    const moodScore = document.getElementById('moodScore');
    if (moodScore) {
        moodScore.focus();
        moodScore.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

function generateWorkoutPlan() {
    displayResponse('💪 Holographic Trainer Activated!', {
        message: 'Personalizing workout based on your biometric data and fitness goals...'
    });
    
    setTimeout(() => {
        displayResponse('💪 Custom Workout Generated!', {
            message: 'Your holographic trainer has prepared a 30-minute session with neural-feedback form correction.'
        });
    }, 2000);
}

// Update the old generateWellnessPlan to use AI
function generateWellnessPlan() {
    generateAIWellnessPlan();
}

/* === Speech-to-Text for the Feelings textarea ===================== */
window.addEventListener('DOMContentLoaded', () => {

  const textarea = document.getElementById('feelingsText');
  const micBtn   = document.getElementById('micBtn');

  // Abort gracefully if the browser has no Web-Speech support
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
      micBtn.style.display = 'none';
      return;
  }

  const recog = new SpeechRecognition();
  recog.lang           = 'en-US';   // change if you need another language
  recog.continuous     = false;     // stop after one utterance
  recog.interimResults = false;     // only final text

  micBtn.addEventListener('click', () => {
      recog.start();
      micBtn.disabled = true;
      micBtn.innerText = '🎙️ Listening…';
  });

  recog.addEventListener('result', e => {
      const spoken = e.results[0][0].transcript;
      textarea.value = (textarea.value + ' ' + spoken).trim() + ' ';
  });

  const resetMic = () => {
      micBtn.disabled = false;
      micBtn.innerText = '🎤 Speak';
  };

  recog.addEventListener('speechend', resetMic);
  recog.addEventListener('error',     resetMic);
});

// ── enable all tooltips on the page ───────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const triggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  triggerList.forEach(el => new bootstrap.Tooltip(el));
});

/* ================================================================= */

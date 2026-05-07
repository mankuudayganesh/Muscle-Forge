// API Configuration - UPDATE THIS LINE with your Render backend
const API_BASE_URL = 'https://muscle-forge.onrender.com/api';  // Changed from localhost to Render

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // ==================== CALCULATOR FUNCTIONS ====================
    window.calculateBMI = function() {
        const weight = document.getElementById('bmiWeight').value;
        const height = document.getElementById('bmiHeight').value;
        
        if (!weight || !height) {
            document.getElementById('bmiResult').innerHTML = '<span style="color:#ffaa00;">Please enter both weight and height</span>';
            return;
        }
        
        const bmi = weight / ((height/100) ** 2);
        let category = '';
        let color = '';
        
        if (bmi < 18.5) {
            category = 'Underweight';
            color = '#ffaa00';
        } else if (bmi < 25) {
            category = 'Normal weight';
            color = '#00ff88';
        } else if (bmi < 30) {
            category = 'Overweight';
            color = '#ffaa00';
        } else {
            category = 'Obese';
            color = '#ff4444';
        }
        
        document.getElementById('bmiResult').innerHTML = `<span style="color:${color}; font-size:18px; font-weight:700">BMI: ${bmi.toFixed(1)}</span><br><span style="color:${color};">${category}</span>`;
    };
    
    window.calculateProtein = function() {
        const weight = document.getElementById('proteinWeight').value;
        const goal = document.getElementById('proteinGoal').value;
        
        if (!weight) {
            document.getElementById('proteinResult').innerHTML = '<span style="color:#ffaa00;">Please enter your weight</span>';
            return;
        }
        
        let protein;
        if (goal === 'muscle_gain') {
            protein = weight * 2.0;
        } else if (goal === 'fat_loss') {
            protein = weight * 1.8;
        } else {
            protein = weight * 1.6;
        }
        
        document.getElementById('proteinResult').innerHTML = `<span style="color:#00aaff; font-size:18px; font-weight:700">${Math.round(protein)}g protein/day</span><br><span style="color:#00ff88;">${Math.round(protein/4)}g per meal</span>`;
    };
    
    window.calculateCalories = function() {
        const weight = parseFloat(document.getElementById('calWeight').value);
        const height = parseFloat(document.getElementById('calHeight').value);
        const age = parseInt(document.getElementById('calAge').value);
        const gender = document.getElementById('calGender').value;
        
        if (!weight || !height || !age) {
            document.getElementById('calResult').innerHTML = '<span style="color:#ffaa00;">Please fill all fields</span>';
            return;
        }
        
        let bmr;
        if (gender === 'male') {
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age);
        } else {
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age);
        }
        
        const maintenance = Math.round(bmr * 1.55);
        const muscleGain = maintenance + 300;
        const fatLoss = maintenance - 450;
        
        document.getElementById('calResult').innerHTML = `
            <span style="color:#00aaff; font-size:16px; font-weight:700">Maintenance: ${maintenance} kcal/day</span><br>
            <span style="color:#00ff88;">💪 Muscle Gain: ${muscleGain} kcal</span><br>
            <span style="color:#ffaa00;">🔥 Fat Loss: ${fatLoss} kcal</span>
        `;
    };
    
    // ==================== FORM HANDLING - GENERATE PLAN ====================
    if (document.getElementById('fitnessForm')) {
        
        async function checkBackend() {
            try {
                // Updated to use Render backend health check
                const response = await fetch('https://muscle-forge.onrender.com/health');
                if (response.ok) {
                    console.log('✅ Backend is reachable on Render');
                    return true;
                }
            } catch (error) {
                console.error('❌ Backend not reachable:', error);
                return false;
            }
            return false;
        }
        
        window.handleSubmit = async function(event) {
            event.preventDefault();
            
            const loadingOverlay = document.getElementById('loadingOverlay');
            if (loadingOverlay) loadingOverlay.style.display = 'flex';
            
            const isBackendRunning = await checkBackend();
            if (!isBackendRunning) {
                alert('❌ Cannot connect to backend!\n\nPlease check:\n1. Backend is deployed on Render\n2. Internet connection is working\n3. Backend URL is correct: https://muscle-forge.onrender.com');
                if (loadingOverlay) loadingOverlay.style.display = 'none';
                return;
            }
            
            const selectedGoal = document.querySelector('input[name="goal"]:checked');
            const selectedActivity = document.querySelector('input[name="activity"]:checked');
            const weeklyBudget = parseFloat(document.getElementById('budget').value);
            
            const height = parseFloat(document.getElementById('height').value);
            const weight = parseFloat(document.getElementById('weight').value);
            const age = parseInt(document.getElementById('age').value);
            
            if (isNaN(height) || height < 50 || height > 300) {
                alert('Please enter a valid height between 50-300 cm');
                if(loadingOverlay) loadingOverlay.style.display = 'none';
                return;
            }
            
            if (isNaN(weight) || weight < 10 || weight > 500) {
                alert('Please enter a valid weight between 10-500 kg');
                if(loadingOverlay) loadingOverlay.style.display = 'none';
                return;
            }
            
            if (isNaN(age) || age < 10 || age > 120) {
                alert('Please enter a valid age between 10-120 years');
                if(loadingOverlay) loadingOverlay.style.display = 'none';
                return;
            }
            
            if (isNaN(weeklyBudget) || weeklyBudget < 500) {
                alert('Minimum weekly budget is ₹500');
                if(loadingOverlay) loadingOverlay.style.display = 'none';
                return;
            }
            
            const formData = {
                name: document.getElementById('fullName').value,
                gender: localStorage.getItem('selectedGender') || 'male',
                age: age,
                height: height,
                weight: weight,
                budget: weeklyBudget,
                experience: document.getElementById('experience').value,
                goal: selectedGoal ? selectedGoal.value : 'muscle_gain',
                diet_preference: document.getElementById('diet_preference').value,
                workout_location: document.getElementById('workout_location').value,
                activity_level: selectedActivity ? selectedActivity.value : 'moderate'
            };
            
            if (!formData.name) { 
                alert('Please enter your full name'); 
                if(loadingOverlay) loadingOverlay.style.display = 'none'; 
                return; 
            }
            
            if (!selectedGoal) { 
                alert('Please select a fitness goal'); 
                if(loadingOverlay) loadingOverlay.style.display = 'none'; 
                return; 
            }
            
            if (!selectedActivity) { 
                alert('Please select your activity level'); 
                if(loadingOverlay) loadingOverlay.style.display = 'none'; 
                return; 
            }
            
            const submitBtn = document.querySelector('.submit-btn');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span>⏳ Generating Plan...</span>';
            submitBtn.disabled = true;
            
            try {
                // Using the Render backend URL
                const response = await fetch(`${API_BASE_URL}/generate-plan`, {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(`Server error: ${response.status}`);
                }
                
                const planData = await response.json();
                
                localStorage.setItem('userPlan', JSON.stringify({
                    success: true,
                    ...planData,
                    weekly_budget: weeklyBudget,
                    daily_budget: weeklyBudget / 7,
                    name: formData.name,
                    gender: formData.gender,
                    diet_preference: formData.diet_preference
                }));
                
                submitBtn.innerHTML = '✓ Plan Generated!';
                submitBtn.style.background = 'linear-gradient(135deg, #00ff88, #00cc66)';
                
                setTimeout(() => {
                    window.location.href = 'plan.html';
                }, 500);
                
            } catch (error) {
                console.error('Error:', error);
                if (loadingOverlay) loadingOverlay.style.display = 'none';
                alert('❌ Failed to generate plan!\n\nBackend URL: https://muscle-forge.onrender.com\n\nError: ' + error.message);
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        };
        
        document.getElementById('fitnessForm').addEventListener('submit', window.handleSubmit);
    }
    
    // ==================== GENDER SELECTION ====================
    if (document.querySelector('.gender-card')) {
        window.selectGender = function(gender) {
            localStorage.setItem('selectedGender', gender);
            const card = event.currentTarget;
            card.style.transform = 'scale(0.96)';
            card.style.boxShadow = '0 0 80px rgba(0,170,255,0.5)';
            setTimeout(() => {
                document.body.style.transition = 'opacity 0.4s';
                document.body.style.opacity = '0';
                setTimeout(() => { window.location.href = 'form.html'; }, 400);
            }, 250);
        };
    }
    
    // ==================== MOBILE NAVIGATION ====================
    window.toggleMobile = function() {
        const mobileNav = document.getElementById('mobileNav');
        if (mobileNav) mobileNav.classList.toggle('open');
    };
    
    window.closeMobile = function() {
        const mobileNav = document.getElementById('mobileNav');
        if (mobileNav) mobileNav.classList.remove('open');
    };
    
    // ==================== SCROLL EFFECTS ====================
    window.addEventListener('scroll', function() {
        const navbar = document.getElementById('navbar');
        if (navbar) {
            navbar.classList.toggle('scrolled', window.scrollY > 50);
        }
    });
    
    // ==================== SCROLL REVEAL ====================
    function revealAll() {
        document.querySelectorAll('.reveal').forEach((el, i) => {
            if (el.getBoundingClientRect().top < window.innerHeight - 60) {
                setTimeout(() => el.classList.add('active'), i * 100);
            }
        });
    }
    
    // ==================== COUNTER ANIMATION ====================
    function animateCounter(el, target, suffix = '') {
        let current = 0;
        const increment = target / 80;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            if (el) el.textContent = Math.floor(current).toLocaleString() + suffix;
        }, 25);
    }
    
    let countersStarted = false;
    function startCounters() {
        if (countersStarted) return;
        const stats = document.querySelector('.stats-container');
        if (stats && stats.getBoundingClientRect().top < window.innerHeight) {
            countersStarted = true;
            const c1 = document.getElementById('counter1');
            const c2 = document.getElementById('counter2');
            const c3 = document.getElementById('counter3');
            if (c1) animateCounter(c1, 10000, '+');
            if (c2) animateCounter(c2, 1999);
            if (c3) animateCounter(c3, 92);
        }
    }
    
    // ==================== 3D TILT EFFECTS ====================
    function initTiltEffects() {
        document.querySelectorAll('.gender-card').forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const r = card.getBoundingClientRect();
                const x = (e.clientX - r.left) / r.width - 0.5;
                const y = (e.clientY - r.top) / r.height - 0.5;
                card.style.transform = `perspective(800px) rotateY(${x * 12}deg) rotateX(${-y * 8}deg) translateY(-15px) scale(1.02)`;
            });
            card.addEventListener('mouseleave', () => { card.style.transform = ''; });
        });
        
        document.querySelectorAll('.feature-card').forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const r = card.getBoundingClientRect();
                const x = (e.clientX - r.left) / r.width - 0.5;
                const y = (e.clientY - r.top) / r.height - 0.5;
                card.style.transform = `perspective(600px) rotateY(${x * 8}deg) rotateX(${-y * 6}deg) translateY(-10px) scale(1.02)`;
            });
            card.addEventListener('mouseleave', () => { card.style.transform = ''; });
        });
        
        document.querySelectorAll('.testimonial-card').forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const r = card.getBoundingClientRect();
                const x = (e.clientX - r.left) / r.width - 0.5;
                const y = (e.clientY - r.top) / r.height - 0.5;
                card.style.transform = `perspective(600px) rotateY(${x * 6}deg) rotateX(${-y * 4}deg) translateY(-8px) scale(1.01)`;
            });
            card.addEventListener('mouseleave', () => { card.style.transform = ''; });
        });
        
        document.querySelectorAll('.stat').forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const r = card.getBoundingClientRect();
                const x = (e.clientX - r.left) / r.width - 0.5;
                const y = (e.clientY - r.top) / r.height - 0.5;
                card.style.transform = `perspective(500px) rotateY(${x * 10}deg) rotateX(${-y * 8}deg) translateY(-8px) scale(1.03)`;
            });
            card.addEventListener('mouseleave', () => { card.style.transform = ''; });
        });
    }
    
    // ==================== THREE.JS ANIMATION ====================
    function initThreeJS() {
        const canvas = document.getElementById('bgCanvas');
        if (!canvas) return;
        
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x050510);
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 20;
        
        const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setClearColor(0x000000, 0);
        
        scene.add(new THREE.AmbientLight(0x0a0a30, 0.3));
        const pL1 = new THREE.PointLight(0x0066ff, 1, 50);
        pL1.position.set(-8, 5, 5);
        scene.add(pL1);
        
        const tkGeo = new THREE.TorusKnotGeometry(2.5, 0.35, 256, 32, 3, 5);
        const tkMat = new THREE.MeshStandardMaterial({ color: 0x0077ff, emissive: 0x001a44, roughness: 0.12, metalness: 0.92 });
        const torusKnot = new THREE.Mesh(tkGeo, tkMat);
        scene.add(torusKnot);
        
        const pCount = 2000;
        const pGeo = new THREE.BufferGeometry();
        const pPos = new Float32Array(pCount * 3);
        for (let i = 0; i < pCount; i++) {
            pPos[i*3] = (Math.random()-0.5) * 200;
            pPos[i*3+1] = (Math.random()-0.5) * 100;
            pPos[i*3+2] = (Math.random()-0.5) * 100 - 30;
        }
        pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
        const particles = new THREE.Points(pGeo, new THREE.PointsMaterial({ color: 0x4488ff, size: 0.05, transparent: true, opacity: 0.3 }));
        scene.add(particles);
        
        let time = 0;
        function animate() {
            requestAnimationFrame(animate);
            time += 0.01;
            torusKnot.rotation.x = time * 0.3;
            torusKnot.rotation.y = time * 0.2;
            particles.rotation.y = time * 0.02;
            renderer.render(scene, camera);
        }
        animate();
        
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    }
    
    // Initialize everything
    setTimeout(() => {
        document.body.classList.add('loaded');
        const mainContent = document.getElementById('mainContent');
        if (mainContent) mainContent.classList.add('visible');
    }, 100);
    
    revealAll();
    window.addEventListener('scroll', revealAll);
    window.addEventListener('scroll', startCounters);
    setTimeout(startCounters, 500);
    initTiltEffects();
    initThreeJS();
});

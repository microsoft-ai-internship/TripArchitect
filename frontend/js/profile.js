    // DOM Elements
    const editPrefBtn = document.getElementById('edit-preferences');
    const prefTest = document.getElementById('preference-test');
    const prefResults = document.getElementById('preference-results');
    const prevBtn = document.getElementById('prev-question');
    const nextBtn = document.getElementById('next-question');
    const progressBar = document.getElementById('progress-bar');
    const questionContainers = document.querySelectorAll('.question-container');
    const optionCards = document.querySelectorAll('.option-card');

    // Test State
    let currentQuestion = 1;
    const totalQuestions = 20;
    const userPreferences = {
      food: [],
      activities: [],
      time: [],
      budget: [],
      transportation: [],
      accommodation: [],
      pace: [],
      company: [],
      climate: [],
      photography: [],
      shopping: [],
      nightlife: [],
      nature: [],
      museums: [],
      local_interaction: [],
      language: [],
      planning: [],
      technology: [],
      wellness: [],
      priority: []
    };

    // Initialize
    function init() {
      // Load theme preference
      if (localStorage.getItem('theme') === 'dark' ||
          (window.matchMedia('(prefers-color-scheme: dark)').matches && !localStorage.getItem('theme'))) {
        document.documentElement.classList.add('dark');
      }

      // Load saved preferences if exists
      const savedPrefs = localStorage.getItem('travelPreferences');
      if (savedPrefs) {
        try {
          Object.assign(userPreferences, JSON.parse(savedPrefs));
          updateResultsDisplay();
        } catch (e) {
          console.error('Error loading preferences:', e);
        }
      }

      // Update progress bar
      updateProgress();
    }

    // Edit Preferences
    editPrefBtn.addEventListener('click', function() {
      prefTest.style.display = 'block';
      prefResults.style.display = 'none';
      this.style.display = 'none';
    });

    // Option Selection
    optionCards.forEach(card => {
      card.addEventListener('click', function() {
        // Remove selected class from siblings
        this.parentNode.querySelectorAll('.option-card').forEach(c => {
          c.classList.remove('selected');
        });

        // Add selected class to clicked card
        this.classList.add('selected');
      });
    });

    // Navigation
    nextBtn.addEventListener('click', function() {
      if (currentQuestion < totalQuestions) {
        // Save answer
        saveAnswer();

        // Move to next question
        document.querySelector(`.question-container[data-question="${currentQuestion}"]`).classList.remove('active');
        currentQuestion++;
        document.querySelector(`.question-container[data-question="${currentQuestion}"]`).classList.add('active');

        // Update buttons and progress
        updateNavigation();
        updateProgress();
      } else {
        // Test completed
        completeTest();
      }
    });

    prevBtn.addEventListener('click', function() {
      if (currentQuestion > 1) {
        document.querySelector(`.question-container[data-question="${currentQuestion}"]`).classList.remove('active');
        currentQuestion--;
        document.querySelector(`.question-container[data-question="${currentQuestion}"]`).classList.add('active');

        updateNavigation();
        updateProgress();
      }
    });

    // Helper Functions
    function saveAnswer() {
      const activeQuestion = document.querySelector(`.question-container[data-question="${currentQuestion}"]`);
      const selectedOption = activeQuestion.querySelector('.option-card.selected');

      if (selectedOption) {
        const value = selectedOption.dataset.value;
        const category = getCategoryForQuestion(currentQuestion);

        if (category && !userPreferences[category].includes(value)) {
          userPreferences[category].push(value);
        }
      }
    }

    function getCategoryForQuestion(questionNum) {
      const categoryMap = {
        1: 'food',
        2: 'activities',
        3: 'time',
        4: 'budget',
        5: 'accommodation',
        6: 'transportation',
        7: 'pace',
        8: 'company',
        9: 'climate',
        10: 'photography',
        11: 'shopping',
        12: 'nightlife',
        13: 'nature',
        14: 'museums',
        15: 'local_interaction',
        16: 'language',
        17: 'planning',
        18: 'technology',
        19: 'wellness',
        20: 'priority'
      };
      return categoryMap[questionNum];
    }

    function updateNavigation() {
      prevBtn.disabled = currentQuestion === 1;
      if (currentQuestion === totalQuestions) {
        nextBtn.innerHTML = 'Bitir <i class="fas fa-check"></i>';
      } else {
        nextBtn.innerHTML = 'Sonraki <i class="fas fa-arrow-right"></i>';
      }
    }

    function updateProgress() {
      const progress = (currentQuestion / totalQuestions) * 100;
      progressBar.style.width = `${progress}%`;
    }

    function completeTest() {
      // Save preferences to localStorage
      localStorage.setItem('travelPreferences', JSON.stringify(userPreferences));

      // Hide test and show results
      prefTest.style.display = 'none';
      prefResults.style.display = 'block';
      editPrefBtn.style.display = 'inline-flex';

      // Reset test state
      currentQuestion = 1;
      document.querySelector(`.question-container[data-question="1"]`).classList.add('active');
      document.querySelector(`.question-container[data-question="${totalQuestions}"]`).classList.remove('active');
      updateProgress();
      updateNavigation();

      // Update results display
      updateResultsDisplay();

      alert('Tercihleriniz başarıyla kaydedildi! Artık önerileriniz bu tercihlere göre şekillenecek.');
    }

    function updateResultsDisplay() {
      const categories = {
        food: { title: 'Yemek Tercihleri', icon: 'fa-utensils' },
        activities: { title: 'Aktivite Tercihleri', icon: 'fa-archway' },
        time: { title: 'Zaman Tercihleri', icon: 'fa-moon' },
        budget: { title: 'Bütçe Tercihleri', icon: 'fa-wallet' },
        transportation: { title: 'Ulaşım Tercihleri', icon: 'fa-bus' },
        accommodation: { title: 'Konaklama Tercihleri', icon: 'fa-hotel' },
        pace: { title: 'Seyahat Temposu', icon: 'fa-tachometer-alt' },
        company: { title: 'Seyahat Arkadaşı', icon: 'fa-users' },
        climate: { title: 'İklim Tercihleri', icon: 'fa-cloud-sun' },
        photography: { title: 'Fotoğraf Çekme', icon: 'fa-camera' },
        shopping: { title: 'Alışveriş Tercihleri', icon: 'fa-shopping-bag' },
        nightlife: { title: 'Gece Hayatı', icon: 'fa-moon' },
        nature: { title: 'Doğa Aktivitesi', icon: 'fa-tree' },
        museums: { title: 'Müze İlgisi', icon: 'fa-landmark' },
        local_interaction: { title: 'Yerel Etkileşim', icon: 'fa-handshake' },
        language: { title: 'Dil Öğrenme', icon: 'fa-language' },
        planning: { title: 'Planlama Stili', icon: 'fa-clipboard-list' },
        technology: { title: 'Teknoloji Kullanımı', icon: 'fa-laptop' },
        wellness: { title: 'Wellness Aktivitesi', icon: 'fa-spa' },
        priority: { title: 'Öncelikler', icon: 'fa-star' }
      };

      let resultsHTML = '';

      for (const [category, data] of Object.entries(categories)) {
        if (userPreferences[category] && userPreferences[category].length > 0) {
          resultsHTML += `
            <div class="preference-category">
              <h4 class="category-title">
                <i class="fas ${data.icon}"></i>
                ${data.title}
              </h4>
              <div class="preference-tags">
                ${userPreferences[category].map(pref =>
                  `<span class="tag">${formatPreferenceText(pref)}</span>`
                ).join('')}
              </div>
            </div>
          `;
        }
      }

      prefResults.innerHTML = resultsHTML;
    }

    function formatPreferenceText(value) {
      const textMap = {
        'traditional': 'Geleneksel Lezzetler',
        'modern': 'Modern Mutfaklar',
        'street': 'Sokak Lezzetleri',
        'fine': 'Lüks Restoranlar',
        'historical': 'Tarihi Mekanlar',
        'nature': 'Doğa Aktivitesi',
        'shopping': 'Alışveriş Mekanları',
        'morning': 'Sabah Etkinlikleri',
        'day': 'Gün İçi Aktiviteler',
        'evening': 'Akşamüstü',
        'night': 'Gece Aktiviteleri',
        'budget': 'Ekonomik Bütçe',
        'moderate': 'Orta Bütçe',
        'luxury': 'Lüks Bütçe',
        'mixed': 'Karma Bütçe',
        'hotel': 'Otel Konaklama',
        'hostel': 'Hostel',
        'apartment': 'Daire',
        'unique': 'Benzersiz Konaklama',
        'walking': 'Yürüyerek',
        'public': 'Toplu Taşıma',
        'taxi': 'Taksi/Uber',
        'rental': 'Araç Kiralama',
        'relaxed': 'Rahat Tempo',
        'balanced': 'Dengeli Tempo',
        'active': 'Aktif Tempo',
        'adventure': 'Macera Tempo',
        'solo': 'Yalnız Seyahat',
        'couple': 'Çift Seyahat',
        'friends': 'Arkadaşlarla',
        'family': 'Aile Seyahat',
        'warm': 'Sıcak İklim',
        'mild': 'Ilıman İklim',
        'cool': 'Serin İklim',
        'cold': 'Soğuk İklim',
        'photo_enthusiast': 'Fotoğraf Tutkunu',
        'photo_some': 'Ara Sıra Fotoğraf',
        'photo_minimal': 'Az Fotoğraf',
        'photo_none': 'Fotoğraf Yok',
        'shopping_heavy': 'Yoğun Alışveriş',
        'shopping_some': 'Biraz Alışveriş',
        'shopping_little': 'Az Alışveriş',
        'shopping_none': 'Alışveriş Yok',
        'nightlife_vibrant': 'Canlı Gece Hayatı',
        'nightlife_cultural': 'Kültürel Gece',
        'nightlight_relaxed': 'Sakin Gece',
        'nightlife_none': 'Gece Hayatı Yok',
        'nature_high': 'Yoğun Doğa',
        'nature_medium': 'Orta Doğa',
        'nature_low': 'Az Doğa',
        'nature_none': 'Doğa Yok',
        'museums_high': 'Müze Tutkunu',
        'museums_selective': 'Seçici Müze',
        'museums_occasional': 'Ara Sıra Müze',
        'museums_none': 'Müze Yok',
        'local_high': 'Yoğun Etkileşim',
        'local_medium': 'Orta Etkileşim',
        'local_low': 'Az Etkileşim',
        'local_none': 'Etkileşim Yok',
        'language_enthusiast': 'Dil Öğrenme',
        'language_basic': 'Temel Dil',
        'language_app': 'Uygulama ile',
        'language_none': 'Dil Yok',
        'planning_detailed': 'Detaylı Plan',
        'planning_structured': 'Yapılandırılmış',
        'planning_flexible': 'Esnek Plan',
        'planning_spontaneous': 'Spontane',
        'tech_heavy': 'Yoğun Teknoloji',
        'tech_medium': 'Orta Teknoloji',
        'tech_light': 'Hafif Teknoloji',
        'tech_none': 'Teknoloji Yok',
        'wellness_high': 'Yoğun Wellness',
        'wellness_medium': 'Orta Wellness',
        'wellness_low': 'Az Wellness',
        'wellness_none': 'Wellness Yok',
        'priority_culture': 'Kültür Öncelikli',
        'priority_food': 'Yemek Öncelikli',
        'priority_adventure': 'Macera Öncelikli',
        'priority_relaxation': 'Rahatlık Öncelikli'
      };

      return textMap[value] || value;
    }

    // Run when DOM is loaded
    document.addEventListener('DOMContentLoaded', init);
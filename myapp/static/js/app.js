document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;

            console.log(page);
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary
        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {
            e.preventDefault();
            this.currentStep++;
            this.updateForm();
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }

    const categoryCheckboxes = document.querySelectorAll('input[name="categories"]');
    const institutionRadios = document.querySelectorAll('input[type="radio"]');
    const nextButton = document.getElementById('nextButton');
    const nextButtonCat = document.getElementById('nextButtonCat');
    const NoInstitutions = document.getElementById('noInstitutions');

    function checkSelectedRadio() {
        let anyRadioSelected = false;
        institutionRadios.forEach(radio => {
            if (radio.checked) {
                anyRadioSelected = true;
            }
        });

        if (!anyRadioSelected) {
            nextButton.style.display = 'none';
        } else {
            nextButton.style.display = '';
        }
    }
    institutionRadios.forEach(radio => {
    radio.addEventListener('change', checkSelectedRadio);
    });
    checkSelectedRadio();
    function filterInstitutions() {
        const selectedCategories = Array.from(categoryCheckboxes)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => parseInt(checkbox.value));

        const isAnyInstitutionVisible = Array.from(institutionRadios).some(radio => {
            const categories = radio.getAttribute('data-categories').split(' ').map(id => parseInt(id));
            return selectedCategories.every(category => categories.includes(category));
        });

        if (!isAnyInstitutionVisible) {
            NoInstitutions.style.display = '';
        } else {
            NoInstitutions.style.display = 'none';
        }

        if (selectedCategories.length === 0) {
            nextButtonCat.style.display = 'none';
        } else {
            nextButtonCat.style.display = '';
        }

        institutionRadios.forEach(radio => {
            const categories = radio.getAttribute('data-categories').split(' ').map(id => parseInt(id));
            const isVisible = selectedCategories.every(category => categories.includes(category));
            if (isVisible) {
                radio.parentNode.style.display = '';
            } else {
                radio.parentNode.style.display = 'none';
            }
        });
    }
    categoryCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', filterInstitutions);
    });
    filterInstitutions();

});
// Znajdź pole input
const bagsInput = document.getElementById('bagsInput');

// Znajdź przycisk "Dalej"
const bagsInputNextButton = document.getElementById('bagsInputNextButton');

// Dodaj nasłuchiwanie na zdarzenie input na polu input
bagsInput.addEventListener('input', function() {
    // Sprawdź, czy pole input zawiera jakieś dane
    if (bagsInput.value.trim() !== '') {
        // Jeśli tak, pokaż przycisk "Dalej"
        bagsInputNextButton.style.display = 'block';
    } else {
        // W przeciwnym razie ukryj przycisk "Dalej"
        bagsInputNextButton.style.display = 'none';
    }
});
const checkInfoButton = document.getElementById('checkInfo');
const summaryItems = document.getElementById('summaryItems');
const address = document.getElementById('address');
const city = document.getElementById('city');
const postcode = document.getElementById('postcode');
const phone = document.getElementById('phone');
const date = document.getElementById('date');
const time = document.getElementById('time');
const more_info = document.getElementById('more_info');

checkInfoButton.addEventListener('click', function() {
    // Pobierz wartości pól formularza
    const bags = document.querySelector('input[name="bags"]').value;

    const organization = document.querySelector('input[name="organization"]:checked');
    const organizationName = organization ? organization.parentNode.querySelector('.title').innerText : '';
    const addressValue = document.querySelector('input[name="address"]').value;
    const cityValue = document.querySelector('input[name="city"]').value;
    const postcodeValue = document.querySelector('input[name="postcode"]').value;
    const phoneValue = document.querySelector('input[name="phone"]').value;
    const dateValue = document.querySelector('input[name="data"]').value;
    const timeValue = document.querySelector('input[name="time"]').value;
    const more_infoValue = document.querySelector('textarea[name="more_info"]').value;

    // Wyświetl podsumowanie
    summaryItems.innerHTML = `
    <li>
        <span class="icon icon-bag"></span>
        <span class="summary--text">${bags} worki ubrań w dobrym stanie dla dzieci</span>
    </li>
    <li>
        <span class="icon icon-hand"></span>
        <span class="summary--text">Dary dla "${organizationName}"</span>
    </li>
    `;
    address.innerText = addressValue;
    city.innerText = cityValue;
    postcode.innerText = postcodeValue;
    phone.innerText = phoneValue;
    date.innerText = dateValue;
    time.innerText = timeValue;
    more_info.innerText = more_infoValue;
});

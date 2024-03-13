document.addEventListener("DOMContentLoaded", ()=>{


    
    
    function toggleForms(showForm) {
        const loginForm = document.querySelector('.login-form');
        const registrationForm = document.querySelector('.registration-form');
        const forgotPasswordForm = document.querySelector('.forgot-password-form');
        const loginLink = document.querySelector('.login-link');

        loginForm.style.display = 'none';
        registrationForm.style.display = 'none';
        forgotPasswordForm.style.display = 'none';
        
        if (showForm === 'login') {
        loginForm.style.display = 'flex';
        } else if (showForm === 'register') {
        registrationForm.style.display = 'flex';
        } else if (showForm === 'forgot-password') {
        forgotPasswordForm.style.display = 'flex';
        }
    }


    //functions to the event listeners
    function showLoginForm() {
        toggleForms('login');
    }

    function showForgotPasswordForm() {
        toggleForms('forgot-password');
    }

    function showRegistrationForm() {
        toggleForms('register');
    }

    let forgotPasswordLink = document.querySelector("#forgot-password-link");
    let registeredLink = document.querySelector("#registered");
    let loginLinks = document.querySelectorAll(".login-link")

    // login page eventlisteners 
    if (forgotPasswordLink){
        forgotPasswordLink.addEventListener("click", showForgotPasswordForm)
    }

    if (registeredLink){
        registeredLink.addEventListener("click", showRegistrationForm)
    }
    if (loginLinks){
        loginLinks.forEach((loginLink)=>{
        loginLink.addEventListener("click", showLoginForm)
        });
    }

    // Drag drop functions -------------------------
    const handleDrop = event => {
        let loading = document.getElementById("loading-box")
        loading.classList.toggle("hide")
        
        console.log("File processing")
        event.preventDefault();
        const {files} = event.dataTransfer;
        handleFiles(files);
    };


    const handleFiles = files => {
        const formData = new FormData();
        for (const file of files) {
        formData.append('file', file);
        }

        // Use fetch to send the files to the server
        fetch('drag-drop', {
        method: 'POST',
        body: formData,
        })
        .then(response => response.json())
        .then(data => {
        // Display the server response (if needed)
        console.log(data);
        window.location.href="/"
        })
        .catch(error => console.error('Error:', error));
    };

    // submit form automitically on upload 
    let fileinput = document.querySelector("#music-input")
    let musicSubmitForm = document.querySelector("#music-form")
    if (fileinput){
        fileinput.addEventListener("change", ()=>{
        let loading = document.getElementById("loading-box")
        loading.classList.toggle("hide")
        musicSubmitForm.submit()
        })
    }

    let myMusicButton = document.querySelector("#my-music-list");
    let musicSection = document.querySelector("#music-section");

    if (myMusicButton){
        myMusicButton.addEventListener("click", ()=>{
            musicSection.classList.toggle("hide")
        })
    }

    // drop area functionality 
    let dropArea = document.querySelector("#drop-area")
    if (dropArea){
        dropArea.addEventListener("drop", handleDrop)
        dropArea.addEventListener("dragover", (event)=>{
            event.preventDefault()
        })
    }

    //Spacebar play function
    let audio = document.querySelector("#audio-bar")
    if (audio){
        document.addEventListener("keydown", event =>{
            if (event.key === " ") {
                if (audio.paused){
                    audio.play()
                    console.log("Played ...")
                }else {
                    audio.play()
                    console.log("Paused ...")
                }
            }
        })
    }
    
    // alert message 
    let alert = document.getElementById("message-alert")
    if (alert){
        setTimeout(()=>{
            alert.classList.toggle("hide")
        }, 8000)
    }

    
})
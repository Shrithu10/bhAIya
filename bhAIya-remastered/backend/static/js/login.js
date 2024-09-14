import { handleGoogleSignIn } from './firebase-auth.js';

document.addEventListener('DOMContentLoaded', function() {
    
    const userToggleButton = document.querySelectorAll('.toggle-button')[0];
    const adminToggleButton = document.querySelectorAll('.toggle-button')[1];
    const loginForm = document.querySelector('.login-form');
    const inputGroups = document.querySelectorAll('.input-group');
    const userTypeInput = document.querySelector('input[name="user_type"]');

    const googleLoginButton = document.getElementById('google-connect');
    if (googleLoginButton) {
        googleLoginButton.addEventListener('click', function(e) {
            e.preventDefault();
            handleGoogleSignIn();
        });
    }

    userToggleButton.addEventListener('click', function() {
        setActiveToggle(userToggleButton, adminToggleButton, 'user');
    });

    adminToggleButton.addEventListener('click', function() {
        setActiveToggle(adminToggleButton, userToggleButton, 'admin');
    });

    function setActiveToggle(activeButton, inactiveButton, role) {
        activeButton.classList.add('active');
        inactiveButton.classList.remove('active');
        userTypeInput.value = role;
    }

    function checkFilled(input) {
        if (input.value.trim() !== "") {
            input.parentElement.classList.add("filled");
        } else {
            input.parentElement.classList.remove("filled");
        }
    }

    inputGroups.forEach(group => {
        const input = group.querySelector('.input-bubble');
        input.addEventListener('input', function() {
            checkFilled(this);
        });

        input.addEventListener('focus', function() {
            group.classList.add('active');
        });

        input.addEventListener('blur', function() {
            group.classList.remove('active');
            checkFilled(this);
        });
    });
});

const scrollingContainer = document.querySelector('.scrolling-text-container');
const scrollSpeed = 2; // Adjusted scroll speed
const interval = 40; // Interval in milliseconds

function autoScroll() {
  scrollingContainer.scrollTop += scrollSpeed;
  console.log('Scroll Top:', scrollingContainer.scrollTop);

  // Add a small buffer to account for rounding issues
  if (scrollingContainer.scrollTop + scrollingContainer.clientHeight >= scrollingContainer.scrollHeight - 1) {
    console.log('Reached bottom, resetting...');
    scrollingContainer.scrollTop = 0;
  }
}

setInterval(autoScroll, interval);





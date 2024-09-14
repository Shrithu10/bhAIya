// firebase-auth.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.4/firebase-app.js";
import { getAuth, signInWithPopup, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/10.12.4/firebase-auth.js";

const firebaseConfig = {
    apiKey: "AIzaSyAUDDGcezlfJFL7YYLjfOHVA8L15LHWt1o",
    authDomain: "bhaiya-ee84c.firebaseapp.com",
    projectId: "bhaiya-ee84c",
    storageBucket: "bhaiya-ee84c.appspot.com",
    messagingSenderId: "183878456700",
    appId: "1:183878456700:web:64968e248795cd9afd00f9",
    measurementId: "G-SHD20ND580"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

function handleGoogleSignIn() {
    const provider = new GoogleAuthProvider();
    signInWithPopup(auth, provider)
        .then((result) => {
            return result.user.getIdToken();
        })
        .then((idToken) => {
            // Send the ID token to your server
            return fetch('/verify_token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ idToken: idToken }),
            });
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                window.location.href = '/index';  // Redirect to main interface
            } else {
                console.error('Authentication failed');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

// Export the function so it can be used in other scripts
export { handleGoogleSignIn };
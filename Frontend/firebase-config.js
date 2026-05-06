// firebase-config.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { 
    getAuth, 
    signInWithEmailAndPassword, 
    createUserWithEmailAndPassword, 
    signInWithPopup, 
    GoogleAuthProvider, 
    sendPasswordResetEmail, 
    signOut, 
    onAuthStateChanged 
} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
import { 
    getFirestore, 
    doc, 
    setDoc, 
    getDoc, 
    updateDoc,
    collection, 
    addDoc, 
    query, 
    where, 
    getDocs, 
    orderBy, 
    arrayUnion 
} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";

// YOUR ACTUAL FIREBASE CONFIGURATION
const firebaseConfig = {
    apiKey: "AIzaSyBYtXjwk59A6x0X6UmUcxFDtPZUMjeAv4c",
    authDomain: "muscle-forge-cfaac.firebaseapp.com",
    databaseURL: "https://muscle-forge-cfaac-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "muscle-forge-cfaac",
    storageBucket: "muscle-forge-cfaac.firebasestorage.app",
    messagingSenderId: "241207291525",
    appId: "1:241207291525:web:626077985a775794ce03ec"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const googleProvider = new GoogleAuthProvider();

// Export all necessary modules
export { 
    auth, 
    db, 
    signInWithEmailAndPassword, 
    createUserWithEmailAndPassword, 
    signInWithPopup, 
    GoogleAuthProvider, 
    sendPasswordResetEmail, 
    signOut, 
    onAuthStateChanged,
    doc, 
    setDoc, 
    getDoc, 
    updateDoc,
    collection, 
    addDoc, 
    query, 
    where, 
    getDocs, 
    orderBy, 
    arrayUnion,
    googleProvider
};
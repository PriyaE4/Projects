<?php
session_start();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = filter_input(INPUT_POST, 'username', FILTER_SANITIZE_STRING);
    $password = filter_input(INPUT_POST, 'password', FILTER_SANITIZE_STRING);

    // DB connection
    $conn = new mysqli("localhost", "root", "", "revivdb");

    if ($conn->connect_error) {
        die("❌ Connection failed: " . $conn->connect_error);
    }

    // Check user credentials
    $stmt = $conn->prepare("SELECT fullname, username, address, email, password FROM users WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result && $result->num_rows === 1) {
        $user = $result->fetch_assoc();

        if ($user['password'] === $password) { // Note: Use hashed password in production

            // Store user info in session
            $_SESSION['username'] = $user['username'];
            $_SESSION['fullname'] = $user['fullname'];
            $_SESSION['email'] = $user['email'];
            $_SESSION['address'] = $user['address'];

            // Redirect to profile
            header("Location: profile.php");
            exit();
        } else {
            echo "❌ Incorrect password.";
        }
    } else {
        echo "⚠ User not found.";
    }

    $stmt->close();
    $conn->close();
} else {
    header("Location: login.html");
    exit();
}
?>

<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get form data
    $username = filter_input(INPUT_POST, 'username', FILTER_SANITIZE_STRING);
    $password = filter_input(INPUT_POST, 'password', FILTER_SANITIZE_STRING);

    // Database connection
    $host = "localhost";
    $dbusername = "root";
    $dbpassword = ""; // Use your actual DB password if needed
    $dbname = "revivdb";

    $conn = new mysqli($host, $dbusername, $dbpassword, $dbname);

    if ($conn->connect_error) {
        die("❌ Connect Error: " . $conn->connect_error);
    }

    // Check if user exists
    $stmt = $conn->prepare("SELECT password FROM users WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $stmt->store_result();
    $stmt->bind_result($db_password);
    $stmt->fetch();

    if ($stmt->num_rows > 0) {
        if ($db_password === $password) { // No hashing, direct comparison
            echo "✅ Login successful! Redirecting...";
            header("Refresh: 2; URL=recyclables.html"); // Redirect after 2 sec
            exit();
        } else {
            echo "❌ Incorrect password! Try again.";
        }
    } else {
        echo "⚠ User not found! <a href='register (2).html'>Register here</a>.";
    }

    $stmt->close();
    $conn->close();
} else {
    // Redirect if accessed directly
    header("Location: login.html");
    exit();
}
?>

<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get form data
    $fullname = filter_input(INPUT_POST, 'fullname', FILTER_SANITIZE_STRING);
    $username = filter_input(INPUT_POST, 'username', FILTER_SANITIZE_STRING);
    $address = filter_input(INPUT_POST, 'address', FILTER_SANITIZE_STRING);
    $email = filter_input(INPUT_POST, 'email', FILTER_SANITIZE_EMAIL);
    $password = filter_input(INPUT_POST, 'password', FILTER_SANITIZE_STRING);
    $reenterpassword = filter_input(INPUT_POST, 'reenterpassword', FILTER_SANITIZE_STRING);

    // Check if passwords match
    if ($password !== $reenterpassword) {
        die("❌ Error: Passwords do not match.");
    }

    // Database connection
    $host = "localhost";
    $dbusername = "root";
    $dbpassword = ""; // Use your actual password if set
    $dbname = "revivdb";

    $conn = new mysqli($host, $dbusername, $dbpassword, $dbname);

    // Check for connection errors
    if ($conn->connect_error) {
        die("❌ Connection failed: " . $conn->connect_error);
    }

    // Check if the username or email already exists
    $query = "SELECT id FROM users WHERE username = ? OR email = ?";
    $stmt = $conn->prepare($query);

    if (!$stmt) {
        die("❌ Prepare statement failed: " . $conn->error);
    }

    $stmt->bind_param("ss", $username, $email);
    $stmt->execute();
    $stmt->store_result();

    if ($stmt->num_rows > 0) {
        echo "⚠ You are already registered! Please <a href='login (3).html'>login here</a>.";
    } else {
        // Insert new user if no existing record is found
        $query = "INSERT INTO users (fullname, username, address, email, password) VALUES (?, ?, ?, ?, ?)";
        $stmt = $conn->prepare($query);

        if (!$stmt) {
            die("❌ Prepare failed: " . $conn->error);
        }

        // Bind parameters (plain password, as requested)
        $stmt->bind_param("sssss", $fullname, $username, $address, $email, $password);

        if ($stmt->execute()) {
            header("Location: login (3).html"); // Redirect to login page
            exit();
        } else {
            die("❌ Error executing query: " . $stmt->error);
        }
    }

    $stmt->close();
    $conn->close();
} else {
    // Redirect if accessed directly
    header("Location: register (2).html");
    exit();
}
?>

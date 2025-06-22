<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get form data
    $name = filter_input(INPUT_POST, 'name', FILTER_SANITIZE_STRING);
    $email = filter_input(INPUT_POST, 'email', FILTER_SANITIZE_STRING);
    $message = filter_input(INPUT_POST, 'message', FILTER_SANITIZE_STRING);
    // Database connection settings
    $host = "localhost";
    $username = "root";     // default username in XAMPP
    $password = "";         // default password in XAMPP is empty
    $dbname = "revivdb";   // your database name

    // Create connection
    $conn = new mysqli($host, $username, $password, $dbname);

    // Check connection
    if ($conn->connect_error) {
        die("❌ Connect Error: " . $conn->connect_error);
    }

// Get form data from POST request
$name = $_POST['name'];
$email = $_POST['email'];
$message = $_POST['message'];

// Prevent SQL injection using prepared statements
$stmt = $conn->prepare("INSERT INTO contact_messages (name, email, message) VALUES (?, ?, ?)");
$stmt->bind_param("sss", $name, $email, $message);

// Execute and give feedback
if ($stmt->execute()) {
    echo "<script>alert('Your message has been sent successfully!'); window.location.href='contact.html';</script>";
} else {
    echo "Error: " . $stmt->error;
}

// Close connection
$stmt->close();
$conn->close();

} else {
    // Redirect if accessed directly
    header("Location: contact.html");
    exit();
}?>


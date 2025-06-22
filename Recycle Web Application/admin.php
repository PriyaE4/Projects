<?php
header('Content-Type: application/json');

// Database credentials
$host = "localhost";
$username = "root";
$password = "";
$dbname = "revivdb";

// Connect
$conn = new mysqli($host, $username, $password, $dbname);
if ($conn->connect_error) {
    echo json_encode([]);
    exit;
}

// Query messages
$sql = "SELECT name, email, message FROM contact_messages";
$result = $conn->query($sql);

$messages = [];

if ($result && $result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $messages[] = $row;
    }
}

$conn->close();

// Return JSON
echo json_encode($messages);
?>

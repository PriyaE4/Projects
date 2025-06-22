<?php
session_start();

// Ensure user is logged in
if (!isset($_SESSION['username'])) {
    header("Location: login.html");
    exit();
}

// Pass session values to JavaScript and redirect to HTML
echo "<script>
    localStorage.setItem('username', '" . addslashes($_SESSION['username']) . "');
    localStorage.setItem('fullname', '" . addslashes($_SESSION['fullname']) . "');
    localStorage.setItem('email', '" . addslashes($_SESSION['email']) . "');
    localStorage.setItem('address', '" . addslashes($_SESSION['address']) . "');
    window.location.href = 'profile.html';
</script>";
exit();
?>

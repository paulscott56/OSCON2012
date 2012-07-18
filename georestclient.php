<?php
// create curl resource
$ch = curl_init();

// set url
curl_setopt($ch, CURLOPT_URL, "http://localhost:8080/loc?lat=18.512740000000001&lon=-33.891150000000003&radius=10");

//return the transfer as a string
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

// $output contains the output string
$output = curl_exec($ch);

// close curl resource to free up system resources
curl_close($ch);     

$dataobject = json_decode($output);

var_dump($dataobject);
?>

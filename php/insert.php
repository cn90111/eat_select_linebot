<?php 

//info ==user, database
$servername = "localhost";
$username = "test123";
$password = "test123";
//database information
$databaseName = "finalproject";
//connect dbms
$tableName = "";
$Name = "";
if(!empty($_GET['tableName']))
{
  $tableName = $_GET['tableName'];
  $Name = $_GET['Name'];
}

$con=mysqli_connect($servername, $username, $password,$databaseName);
mysqli_query($con,"SET CHARACTER SET 'utf8'");
//mysqli_query($conn,"SET SESSION collation_connection ='utf8_unicode_ci'");
if ($con->connect_error) 
{
    die("Too bad!!!! Connection failed: " . $con->connect_error);
} 

//connect db
// Change database
mysqli_select_db($con,$tableName);

//insert
$result = mysqli_query($con,"INSERT INTO $tableName (name) VALUES ('".$Name."') ");

if($result)
	echo $result;
else
	echo 0;
//close db
mysqli_close($con);
?>
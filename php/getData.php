<?php 

//info ==user, database
$servername = "localhost";
$username = "test123";
$password = "test123";
//database information
$databaseName = "finalproject";
//connect dbms

$tableName = "";
$id1 = "";
$id2 = "";
if(!empty($_GET['tableName']) &&  !empty($_GET['id1']) && !empty($_GET['id2']))
{
  $tableName = $_GET['tableName'];
  $id1 = $_GET['id1'];
  $id2 = $_GET['id2'];
}

$con=mysqli_connect($servername, $username, $password,$databaseName);
mysqli_query($con,"SET CHARACTER SET 'utf8'");
//mysqli_query($conn,"SET SESSION collation_connection ='utf8_unicode_ci'");
if ($con->connect_error) {
    die("Too bad!!!! Connection failed: " . $con->connect_error);
} 
//echo "Connected successfully !!!! Yayaya.=======...";

//connect db
mysqli_select_db($con,$tableName);

//select
//Query database for data
 
$result= mysqli_query($con,"SELECT name,longitude,latitude from $tableName where id='".$id1."' or id='".$id2."' ");
  //store matrix
  $i=0;
  while ($row = mysqli_fetch_array($result,MYSQLI_NUM)){
    $data[$i]=$row;
    $i++;
  }

  //echo result as json 
  echo json_encode($data,JSON_UNESCAPED_UNICODE);

//close db
mysqli_close($con);

?>



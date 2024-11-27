<?php
    include "connection.php";

    if($_POST["action"] == "infoCont"){
        $id_cont = $_POST["cont"];
        $sql = "SELECT * FROM containers WHERE id_container = \"$id_cont\"";
        $query = mysqli_query($conn,$sql);
        mysqli_close($conn);
        $result = mysqli_num_rows($query);
        if($result>0){
            $data = mysqli_fetch_assoc($query);
            echo(json_encode($data,JSON_UNESCAPED_UNICODE));
            exit;
        }
        exit;
    }

    if($_POST["action"] == "monitorCont"){
        $id_cont = $_POST["cont"];
        $sql = "select * from containers_utility WHERE id_container = \"$id_cont\" ORDER BY timestamp_utility DESC LIMIT 1";
        $query = mysqli_query($conn,$sql);
        mysqli_close($conn);
        $result = mysqli_num_rows($query);
        if($result>0){
            $data = mysqli_fetch_assoc($query);
            echo(json_encode($data,JSON_UNESCAPED_UNICODE));
            exit;
        }
        exit;
    }

    if($_POST["action"] == "CPUCont"){
        $id_cont = $_POST["cont"];
        $sql = "SELECT cpu_level FROM containers_utility WHERE id_container = \"$id_cont\" ORDER BY timestamp_utility DESC LIMIT 10";
        $result1 = $conn->query($sql);
        $data = array('0','0','0','0','0','0','0','0','0','0');
        $i = 0;
        if ($result1->num_rows > 0) {
          while($row = $result1->fetch_assoc()) {
            $data[$i] = $row["cpu_level"];
            $i = $i + 1;
          }
        }
        $data = array_reverse($data);
        echo(json_encode($data,JSON_UNESCAPED_UNICODE));
        exit;
    }

    if($_POST["action"] == "memoryCont"){
      $id_cont = $_POST["cont"];
      $sql = "SELECT memory_level FROM containers_utility WHERE id_container = \"$id_cont\" ORDER BY timestamp_utility DESC LIMIT 10";
      $result1 = $conn->query($sql);
      $data = array('0','0','0','0','0','0','0','0','0','0');
      $i = 0;
      if ($result1->num_rows > 0) {
        while($row = $result1->fetch_assoc()) {
          $data[$i] = $row["memory_level"];
          $i = $i + 1;
        }
      }
      $data = array_reverse($data);
      echo(json_encode($data,JSON_UNESCAPED_UNICODE));
      exit;
    }

    if($_POST["action"] == "networkCont"){
      $id_cont = $_POST["cont"];
      $sql = "SELECT network_level FROM containers_utility WHERE id_container = \"$id_cont\" ORDER BY timestamp_utility DESC LIMIT 10";
      $result1 = $conn->query($sql);
      $data = array('0','0','0','0','0','0','0','0','0','0');
      $i = 0;
      if ($result1->num_rows > 0) {
        while($row = $result1->fetch_assoc()) {
          $data[$i] = $row["network_level"];
          $i = $i + 1;
        }
      }
      $data = array_reverse($data);
      echo(json_encode($data,JSON_UNESCAPED_UNICODE));
      exit;
    }

    if($_POST["action"] == "fsCont"){
      $id_cont = $_POST["cont"];
      $sql = "SELECT fs_level FROM containers_utility WHERE id_container = \"$id_cont\" ORDER BY timestamp_utility DESC LIMIT 10";
      $result1 = $conn->query($sql);
      $data = array('0','0','0','0','0','0','0','0','0','0');
      $i = 0;
      if ($result1->num_rows > 0) {
        while($row = $result1->fetch_assoc()) {
          $data[$i] = $row["fs_level"];
          $i = $i + 1;
        }
      }
      $data = array_reverse($data);
      echo(json_encode($data,JSON_UNESCAPED_UNICODE));
      exit;
    }

    if($_POST["action"] == "appStruct"){
      $name_app = $_POST["app"];

      $sql = "SELECT structure_json FROM applications_graph WHERE name_app = \"$name_app\"";
      $result1 = $conn->query($sql);
      $data = array('0');
      $i = 0;
      if ($result1->num_rows > 0) {
        while($row = $result1->fetch_assoc()) {
          $data[$i] = $row["structure_json"];
          $i = $i + 1;
        }
      }
      echo(json_encode($data,JSON_UNESCAPED_UNICODE));
      exit;
    }

    if($_POST["action"] == "appStatus"){
      $name_app = $_POST["app"];

      $sql = "SELECT status_json FROM applications_graph WHERE name_app = \"$name_app\"";
      $result1 = $conn->query($sql);
      $data = array('0');
      $i = 0;
      if ($result1->num_rows > 0) {
        while($row = $result1->fetch_assoc()) {
          $data[$i] = $row["status_json"];
          $i = $i + 1;
        }
      }
      echo(json_encode($data,JSON_UNESCAPED_UNICODE));
      exit;
    }

    /*if($_POST["action"] == "servicesS"){
      $name_app = $_POST["app"];

      $sql = "SELECT status_json FROM applications_graph WHERE name_app = \"$name_app\"";
      $result1 = $conn->query($sql);
      $data = array('0');
      $i = 0;
      if ($result1->num_rows > 0) {
        while($row = $result1->fetch_assoc()) {
          $data[$i] = $row["status_json"];
          $i = $i + 1;
        }
      }
      echo(json_encode($data,JSON_UNESCAPED_UNICODE));
      exit;
    }*/

?>
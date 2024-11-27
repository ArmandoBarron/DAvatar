<?php
  include "connection.php";
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>WOT Model</title>
  <meta content="width=device-width, initial-scale=1.0" name="viewport">
  <meta content="" name="keywords">
  <meta content="" name="description">

  <!-- Favicons -->
  <link href="img/favicon.png" rel="icon">
  <link href="img/apple-touch-icon.png" rel="apple-touch-icon">

  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,500,600,700,700i|Montserrat:300,400,500,600,700" rel="stylesheet">

  <!-- Bootstrap CSS File -->
  <link href="lib/bootstrap/css/bootstrap.min.css" rel="stylesheet">

  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="bootstrap/css/bootstrap.min.css">

  <!--datables CSS básico-->
  <link rel="stylesheet" type="text/css" href="datatables/datatables.min.css"/>
  <!--datables estilo bootstrap 4 CSS-->  
  <link rel="stylesheet"  type="text/css" href="datatables/DataTables-1.10.18/css/dataTables.bootstrap4.min.css">

  <!-- Libraries CSS Files -->
  <link href="lib/font-awesome/css/font-awesome.min.css" rel="stylesheet">
  <link href="lib/animate/animate.min.css" rel="stylesheet">
  <link href="lib/ionicons/css/ionicons.min.css" rel="stylesheet">
  <link href="lib/owlcarousel/assets/owl.carousel.min.css" rel="stylesheet">
  <link href="lib/lightbox/css/lightbox.min.css" rel="stylesheet">

  <!-- Main Stylesheet File -->
  <link href="css/style.css" rel="stylesheet">
 
  <!-- JSON TREE -->
  <link href="libs/jsonTree/jsonTree.css" rel="stylesheet" />

</head>

<body>
  <!--==========================
  Header
  ============================-->
  <header id="header">

    <div class="container">

      <div class="logo float-left">
        <h1 class="text-light"><a href="index.html" class="scrollto"><span>WoT Model</span></a></h1>
      </div>

      <nav class="main-nav float-right d-none d-lg-block">
        <ul>
          <li><a href="index.html">Home</a></li>
          <li class="drop-down"><a href="">Services</a>
            <ul>
              <li><a href="containers_discovery.php">Container Discovery</a></li>
              <li><a href="containers_monitoring.php">Container Monitoring</a></li>
              <li><a href="apps_discovery.php">Application Discovery</a></li>
            </ul>
          </li>
          <li><a href="#about">About Us</a></li>
          <li><a href="#footer">Contact Us</a></li>
        </ul>
      </nav>
      
    </div>
  </header><!-- #header -->

  <!--==========================
    Intro Section
  ============================-->
  <section id="intro2" class="clearfix">
    <div class="container d-flex h-100">
      <div class="row justify-content-center align-self-center">
      </div>

    </div>
  </section><!-- #intro -->

  <main id="main">

    <!--==========================
      About Us Section
    ============================-->
    <section id="services">

      <div class="container">
        <div class="col-md-12">
            <h2><b>Container Monitoring</b></h2>
            <hr style="border-color:413e66;">
            <br><br>
            <div class="container">
              <div class="row">
                <div class="table-responsive">        
                <table id="example" class="table table-striped table-bordered" style="width:100%">
                    <thead>
                        <tr>
                            <th style= "text-align: center; vertical-align: middle;">Name</th>
                            <th style= "text-align: center; vertical-align: middle;">Status</th>
                            <th style= "text-align: center; vertical-align: middle;">CPU</th>
                            <th style= "text-align: center; vertical-align: middle;">Memory</th>
                            <th style= "text-align: center; vertical-align: middle;">Network</th>
                            <th style= "text-align: center; vertical-align: middle;">FS</th>
                            <th style= "text-align: center; vertical-align: middle;">Info</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php 
                          $sql = "SELECT * FROM containers";
                          $result1 = $conn->query($sql);
                          if ($result1->num_rows > 0) {
                              while($row = $result1->fetch_assoc()) {
                                echo"<tr style= 'text-align: center; vertical-align: middle;'>";
                                echo"<td style= 'text-align: center; vertical-align: middle;'>".$row["name"]."</td>";
                                if($row["status_p"]==1){
                                  echo"<td style= 'text-align: center; vertical-align: middle;'>".$row["status"]."</td>";
                                }
                                else{
                                  echo"<td style= 'text-align: center; vertical-align: middle;'>null</td>";
                                }
                                $id_cont = $row["id_container"];
                                $sql2 = "select * from containers_utility WHERE id_container = \"$id_cont\" ORDER BY timestamp_utility DESC LIMIT 1";
                                $result2 = $conn->query($sql2);

                                if ($result2->num_rows > 0 ) {
                                  while($row2 = $result2->fetch_assoc()) {
                                    if($row2["utility_p"]==1){
                                      if($row2["cpu_level"] == 0){
                                        echo'<td value="'.$row2["cpu_level"].'" style= "text-align: center; vertical-align: middle;"> <div class="" style=""><i class="ion-alert-circled" style="color: #A7A7A7; zoom:2.0;"></i></div> </td>';
                                      }
                                      else{
                                        if($row2["cpu_level"] == 1){
                                          echo'<td value="'.$row2["cpu_level"].'" style= "text-align: center; vertical-align: middle;"> <div class="" style=""><i class="ion-alert-circled" style="color: #00C120; zoom:2.0;"></i></div> </td>';
                                        }
                                        else{
                                          if($row2["cpu_level"] == 2){
                                            echo'<td value="'.$row2["cpu_level"].'" style= "text-align: center; vertical-align: middle;"> <div class="" style=""><i class="ion-alert-circled" style="color: #FFD904; zoom:2.0;"></i></div> </td>';
                                          }
                                          else{
                                            if($row2["cpu_level"] == 3){
                                              echo'<td value="'.$row2["cpu_level"].'" style= "text-align: center; vertical-align: middle;"> <div class="" style=""><i class="ion-alert-circled" style="color: #DA0000; zoom:2.0;"></i></div> </td>';
                                            }
                                          }
                                        }
                                      }

                                      if($row2["memory_level"] == 0){
                                        echo'<td value="'.$row2["memory_level"].'" style= "text-align: center; vertical-align: middle;"> <div class="" style=""><i class="ion-alert-circled" style="color: #A7A7A7; zoom:2.0;"></i></div> </td>';
                                      }
                                      else{
                                        if($row2["memory_level"] == 1){
                                          echo'<td value="'.$row2["memory_level"].'" style= "text-align: center; vertical-align: middle;"> <div class="" style=""><i class="ion-alert-circled" style="color: #00C120; zoom:2.0;"></i></div> </td>';
                                        } 
                                        else{
                                          if($row2["memory_level"] == 2){
                                            echo'<td value="'.$row2["memory_level"].'" style= "text-align: center; vertical-align: middle;"> <div class="" style=""><i class="ion-alert-circled" style="color: #FFD904; zoom:2.0;"></i></div> </td>';
                                          }
                                          else{
                                            if($row2["memory_level"] == 3){
                                              echo'<td value="'.$row2["memory_level"].'" style= "text-align: center; vertical-align: middle;"> <div class="" style=""><i class="ion-alert-circled" style="color: #DA0000; zoom:2.0;"></i></div> </td>';
                                            }
                                          }
                                        }
                                      }

                                      if($row2["network_level"] == 0){
                                        echo'<td value="'.$row2["network_level"].'" style= "text-align: center; vertical-align: middle;"> <div class="" style=""><i class="ion-alert-circled" style="color: #A7A7A7; zoom:2.0;"></i></div> </td>';
                                      }
                                      else{
                                        if($row2["network_level"] == 1){
                                          echo'<td value="'.$row2["network_level"].'" style= "text-align: center; vertical-align: middle;"> <div class="" style=""><i class="ion-alert-circled" style="color: #00C120; zoom:2.0;"></i></div> </td>';
                                        }
                                        else{
                                          if($row2["network_level"] == 2){
                                            echo'<td value="'.$row2["network_level"].'" style= "text-align: center; vertical-align: middle;"> <div class="" style=""><i class="ion-alert-circled" style="color: #FFD904; zoom:2.0;"></i></div> </td>';
                                          }
                                          else{
                                            if($row2["network_level"] == 3){
                                              echo'<td value="'.$row2["network_level"].'" style= "text-align: center; vertical-align: middle;"> <div class="" style=""><i class="ion-alert-circled" style="color: #DA0000; zoom:2.0;"></i></div> </td>';
                                            }
                                          }
                                        }
                                      }

                                      if($row2["fs_level"] == 0){
                                        echo'<td value="'.$row2["fs_level"].'" style= "text-align: center; vertical-align: middle;"> <div class="" style=""><i class="ion-alert-circled" style="color: #A7A7A7; zoom:2.0;"></i></div> </td>';
                                      }
                                      else{
                                        if($row2["fs_level"] == 1){
                                          echo'<td value="'.$row2["fs_level"].'" style= "text-align: center; vertical-align: middle;"> <div class="" style=""><i class="ion-alert-circled" style="color: #00C120; zoom:2.0;"></i></div> </td>';
                                        }
                                        else{
                                          if($row2["fs_level"] == 2){
                                            echo'<td value="'.$row2["fs_level"].'" style= "text-align: center; vertical-align: middle;"> <div class="" style=""><i class="ion-alert-circled" style="color: #FFD904; zoom:2.0;"></i></div> </td>';
                                          }
                                          else{
                                            if($row2["fs_level"] == 3){
                                              echo'<td value="'.$row2["fs_level"].'" style= "text-align: center; vertical-align: middle;"> <div class="" style=""><i class="ion-alert-circled" style="color: #DA0000; zoom:2.0;"></i></div> </td>';
                                            }
                                          }
                                        }
                                      }
                                    }
                                    else{
                                      echo'<td value="'.$row2["cpu_level"].'" style= "text-align: center; vertical-align: middle;"> <div class="" style="">private</div> </td>';
                                      echo'<td value="'.$row2["memory_level"].'" style= "text-align: center; vertical-align: middle;"> <div class="" style="">private</div> </td>';
                                      echo'<td value="'.$row2["network_level"].'" style= "text-align: center; vertical-align: middle;"> <div class="" style="">private</div> </td>';
                                      echo'<td value="'.$row2["fs_level"].'" style= "text-align: center; vertical-align: middle;"> <div class="" style="">private</div> </td>';
                                    }
                                  }
                                }
                                echo"<td style= 'text-align: center; vertical-align: middle;'>".'<button class="more_cont" product="'.$row["id_container"].'" value="More" data-toggle="modal" data-target="#myModal" style="background: #1bb1dc; border: 0; border-radius: 3px; padding: 8px 20px; color: #fff; transition: 0.3s;"> More </button>'."</td>";
                                echo"</tr>";
                              }
                          }
                          echo'
                            <div class="modal" id="myModal" role="dialog">
                            <div class="modal-dialog">
                              <div class="modal-content">
                                <div class="modal-header">
                                  <h3 class="" style="text-align:left; color: #413e66;"><b>Container Info</b></h3>
                                  <button type="button" class="close" data-dismiss="modal" style= "color:#CF0000;">&times;</button>
                                </div>
                                <div class="modal-body">
                                  <p class="id_cont" style="text-align:left"></p>
                                  <p class="cpu_util" style="text-align:left"></p>
                                  <p class="memory_util" style="text-align:left"></p>
                                  <p class="network_util" style="text-align:left"></p>
                                  <p class="fs_util" style="text-align:left"></p>
                                  <p class="timestamp_util" style="text-align:left"></p>
                                </div>
                                <div class="modal-footer">
                                  <a class="record" href="" class="" style="background: #413e66; border: 0; border-radius: 3px; padding: 8px 20px; color: #fff; transition: 0.3s;">Record</a>
                                </div>
                              </div>
                              
                            </div>
                          </div>
                          ';
                        ?>
                    </tbody>        
                  </table>                  
                </div>
            </div>
          </div>  
        </div>
      </div>
      <!-- Modal -->

    </section><!-- #about -->


  </main>

  <a href="#" class="back-to-top"><i class="fa fa-chevron-up"></i></a>
  <!-- Uncomment below i you want to use a preloader -->
  <!-- <div id="preloader"></div> -->

  <!-- JavaScript Libraries -->
  <script src="lib/jquery/jquery.min.js"></script>
  <script src="lib/jquery/jquery-migrate.min.js"></script>
  <script src="lib/bootstrap/js/bootstrap.bundle.min.js"></script>
  <script src="lib/easing/easing.min.js"></script>
  <script src="lib/mobile-nav/mobile-nav.js"></script>
  <script src="lib/wow/wow.min.js"></script>
  <script src="lib/waypoints/waypoints.min.js"></script>
  <script src="lib/counterup/counterup.min.js"></script>
  <script src="lib/owlcarousel/owl.carousel.min.js"></script>
  <script src="lib/isotope/isotope.pkgd.min.js"></script>
  <script src="lib/lightbox/js/lightbox.min.js"></script>
  <script src="https://unpkg.com/ionicons@5.2.3/dist/ionicons.js"></script>
  <!-- Contact Form JavaScript File -->
  <script src="contactform/contactform.js"></script>

  <!-- Template Main Javascript File -->
  <script src="js/main.js"></script>

  <!-- jQuery, Popper.js, Bootstrap JS -->
  <script src="jquery/jquery-3.3.1.min.js"></script>
  <script src="popper/popper.min.js"></script>
  <script src="bootstrap/js/bootstrap.min.js"></script>
    
  <!-- datatables JS -->
  <script type="text/javascript" src="datatables/datatables.min.js"></script>    
    
  <script type="text/javascript" src="main.js"></script>
  
  <!-- JSON TREE VIEW -->
  <script src="libs/jsonTree/jsonTree.js"></script>
  <script>
    $('.more_cont').click(function(e){
      e.preventDefault();
      var cont = $(this).attr('product');
      var action = "monitorCont";

      $.ajax({
        url: "ajax.php",
        type: "POST",
        async: true,
        data: {action:action,cont:cont},
      
        success: function(response){
          console.log(response);

          if(response != "error"){
            var info = JSON.parse(response);
            $(".id_cont").html("ID: ".concat("",info.id_container));
            if(info.utility_p == 1){
              $(".cpu_util").html("CPU Utilization: ".concat("",info.cpu_utility));
              $(".memory_util").html("Memory Utilization: ".concat("",info.memory_utility));
              $(".network_util").html("Network Utilization: ".concat("",info.network_utility));
              $(".fs_util").html("FS Utilization: ".concat("",info.fs_utility));
              $(".timestamp_util").html("Timestamp: ".concat("",info.timestamp_utility));
              var str1 = "containers_record.php?id_cont=".concat("",info.id_container);
              //var str2 = str1.concat("","&name=");
              $(".record").attr("href", str1);
            }
            else{
              $(".cpu_util").html("CPU Utilization: ".concat("","private"));
              $(".memory_util").html("Memory Utilization: ".concat("","private"));
              $(".network_util").html("Network Utilization: ".concat("","private"));
              $(".fs_util").html("FS Utilization: ".concat("","private"));
              $(".timestamp_util").html("Timestamp: ".concat("","private"));
              var str1 = "containers_record.php?id_cont=".concat("","private");
              $(".record").disabled=true;
            }
          }
        },

        error: function(error){
          console.log(error);
        }
      });


      $('.modal').fadeIn();
    });
  </script>

</body>

</html>


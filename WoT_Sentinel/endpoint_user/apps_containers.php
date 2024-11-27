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
            <h2><b>Container(s)</b></h2>
            <hr style="border-color:413e66;">
            <br><br>
            <div class="container">
              <div class="row">
                <div class="table-responsive">        
                    <table id="example" class="table table-striped table-bordered" style="width:100%">
                    <thead>
                        <tr>
                            <th>ID (Docker)</th>
                            <th>Name</th>
                            <th>Status</th>
                            <th>Description</th>
                            <th>Info</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php 
                          $id_app = $_GET["id_app"];
                          
                          $sql = "SELECT * FROM containers INNER JOIN applications_containers ON containers.id_container = applications_containers.id_container WHERE applications_containers.id_app = $id_app";
                          $result1 = $conn->query($sql);
                          $conn->close();
                          if ($result1->num_rows > 0) {
                              while($row = $result1->fetch_assoc()) {
                                echo"<tr>";
                                echo"<td>".$row["id_container"]."</td>";
                                echo"<td>".$row["name"]."</td>";
                                echo"<td>".$row["status"]."</td>";
                                echo"<td>".$row["description"]."</td>";
                                echo"<td>".'<button class="more_cont" product="'.$row["id_container"].'" value="More" data-toggle="modal" data-target="#myModal" style="background: #1bb1dc; border: 0; border-radius: 3px; padding: 8px 20px; color: #fff; transition: 0.3s;"> More </button>'."</td>";
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
                                  <p class="name" style="text-align:left"></p>
                                  <p class="status" style="text-align:left"></p>
                                  <p class="image" style="text-align:left"></p>
                                  <p class="volumes" style="text-align:left"></p>
                                </div>
                                <div class="modal-footer">
                                  <a class="scheme" href="" class="" style="background: #413e66; border: 0; border-radius: 3px; padding: 8px 20px; color: #fff; transition: 0.3s;">TD Scheme</a>
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
      var action = "infoCont";

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
            $(".name").html("Name: ".concat("",info.name));
            $(".status").html("Status: ".concat("",info.status));
            $(".image").html("Image: ".concat("",info.image));
            $(".volumes").html("Volumes: ".concat("",info.volumes));
            var str1 = "containers_scheme.php?id_cont=".concat("",info.id_container);
            var str2 = str1.concat("","&name=");
            $(".scheme").attr("href", str2.concat("",info.name));

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


<?php
  include("connection.php");
  $id_cont = $_GET["id_cont"];
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
        <!-- Uncomment below if you prefer to use an image logo -->
        <h1 class="text-light"><a href="index.html" class="scrollto"><span>WoT Model</span></a></h1>
        <!-- <a href="#header" class="scrollto"><img src="img/logo.png" alt="" class="img-fluid"></a> -->
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
    <section id="about">

      <div class="container">
            <div class="about-content">
              <h2>Record</h2>
              <input id="container" type="hidden" value="<?php echo $id_cont ?>">
              <hr style="border-color:413e66;">
              <br><br>
              <div class="col-md-5 float-left">
                <h3 style="text-align:center;"> <b>CPU Utilization </b></h3>
                <canvas id="lineChartCPU" height="100" width="100"></canvas>
              </div>
              <div class="col-md-5 float-right">
                <h3 style="text-align:center;"> <b>Memory Utilization </b></h3>
                <canvas id="lineChartMemory" height="100" width="100"></canvas>
              </div>
              <div class="col-md-5 float-left">
                <br><br><br>
                  <h3 style="text-align:center;"> <b>Network Utilization </b></h3>
                  <canvas id="lineChartNetwork" height="100" width="100"></canvas>
              </div>
              <div class="col-md-5 float-right">
                <br><br><br>
                <h3 style="text-align:center;"> <b>FS Utilization </b></h3>
                <canvas id="lineChartFS" height="100" width="100"></canvas>
              </div>

            </div>
      </div>

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


<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.min.js"> </script>

<script>
    
    var cont = document.getElementById('container').value;
    $.ajax({
      url: "ajax.php",
      type: "POST",
      async: true,
      data: {action:"CPUCont",cont:cont},
      success: function(response){
        console.log(response);
        if(response != "error"){
          var info = JSON.parse(response);
          const CHART_CPU = document.getElementById("lineChartCPU");
          console.log(CHART_CPU);
          let lineChartCPU = new Chart(CHART_CPU,{
              type: "line",
              data: {
                  labels: ["1", "2", "3", "4", "5", "6", "7","8","9","10"],
                  datasets: [
                      {
                          label: "CPU",
                          fill: false,
                          lineTension: 0.1,
                          backgroundColor: "rgba(63, 205, 199,0.4)",
                          borderColor: "rgba(63, 205, 199,1)",
                          borderCapStyle: 'butt',
                          borderDash: [],
                          borderDashOffset: 0.0,
                          borderJoinStyle: 'miter',
                          pointBorderColor: "rgba(63, 205, 199,1)",
                          pointBackgroundColor: "#fff",
                          pointBorderWidth: 1,
                          pointHoverRadius: 5,
                          pointHitRadius: 10,
                          responsive: true,
                          data: info,
                      }
                  ]
              }
          });
        }
      },

      error: function(error){
        console.log(error);
      }
    });

    $.ajax({
      url: "ajax.php",
      type: "POST",
      async: true,
      data: {action:"memoryCont",cont:cont},
      success: function(response){
        console.log(response);
        if(response != "error"){
          var info = JSON.parse(response);
          const CHART_MEMORY = document.getElementById("lineChartMemory");
          console.log(CHART_MEMORY);
          let lineChartMemory = new Chart(CHART_MEMORY,{
              type: "line",
              data: {
                  labels: ["1", "2", "3", "4", "5", "6", "7","8","9","10"],
                  datasets: [
                      {
                          label: "Memory",
                          fill: false,
                          lineTension: 0.1,
                          backgroundColor: "rgba(254, 125, 125, 0.4)",
                          borderColor: "rgba(254, 125, 125, 1)",
                          borderCapStyle: 'butt',
                          borderDash: [],
                          borderDashOffset: 0.0,
                          borderJoinStyle: 'miter',
                          pointBorderColor: "rgba(254, 125, 125,1)",
                          pointBackgroundColor: "#fff",
                          pointBorderWidth: 1,
                          pointHoverRadius: 5,
                          pointHitRadius: 10,
                          responsive: true,
                          data: info,
                      }
                  ]
              }
          });
        }
      },

      error: function(error){
        console.log(error);
      }
    });

    $.ajax({
      url: "ajax.php",
      type: "POST",
      async: true,
      data: {action:"networkCont",cont:cont},
      success: function(response){
        console.log(response);
        if(response != "error"){
          var info = JSON.parse(response);
          const CHART_NETWORK = document.getElementById("lineChartNetwork");
          console.log(CHART_NETWORK);
          let lineChart_Network = new Chart(CHART_NETWORK,{
              type: "line",
              data: {
                  labels: ["1", "2", "3", "4", "5", "6", "7","8","9","10"],
                  datasets: [
                      {
                          label: "Network",
                          fill: false,
                          lineTension: 0.1,
                          backgroundColor: "rgba(112, 73, 255, 0.4)",
                          borderColor: "rgba(112, 73, 255, 1)",
                          borderCapStyle: 'butt',
                          borderDash: [],
                          borderDashOffset: 0.0,
                          borderJoinStyle: 'miter',
                          pointBorderColor: "rgba(112, 73, 255,1)",
                          pointBackgroundColor: "#fff",
                          pointBorderWidth: 1,
                          pointHoverRadius: 5,
                          pointHitRadius: 10,
                          responsive: true,
                          data: info,
                      }
                  ]
              }
          });
        }
      },

      error: function(error){
        console.log(error);
      }
    });

    $.ajax({
      url: "ajax.php",
      type: "POST",
      async: true,
      data: {action:"fsCont",cont:cont},
      success: function(response){
        console.log(response);
        if(response != "error"){
          var info = JSON.parse(response);
          const CHART_FS = document.getElementById("lineChartFS");
          console.log(CHART_FS);
          let lineChartFS = new Chart(CHART_FS,{
              type: "line",
              data: {
                  labels: ["1", "2", "3", "4", "5", "6", "7","8","9","10"],
                  datasets: [
                      {
                          label: "FS",
                          fill: false,
                          lineTension: 0.1,
                          backgroundColor: "rgba(255, 223, 41, 0.4)",
                          borderColor: "rgba(255, 223, 41, 1)",
                          borderCapStyle: 'butt',
                          borderDash: [],
                          borderDashOffset: 0.0,
                          borderJoinStyle: 'miter',
                          pointBorderColor: "rgba(255, 223, 41,1)",
                          pointBackgroundColor: "#fff",
                          pointBorderWidth: 1,
                          pointHoverRadius: 5,
                          pointHitRadius: 10,
                          responsive: true,
                          data: info,
                      }
                  ]
              }
          });
        }
      },

      error: function(error){
        console.log(error);
      }
    });

    






  /*const CHART_CPU = document.getElementById("lineChartCPU");
  console.log(CHART_CPU);
  let lineChartCPU = new Chart(CHART_CPU,{
      type: "line",
      data: {
          labels: ["January", "February", "March", "April", "May", "June", "July","jsjsjjs","jdjdjd","jdjdkjd"],
          datasets: [
              {
                  label: "CPU",
                  fill: false,
                  lineTension: 0.1,
                  backgroundColor: "rgba(63, 205, 199,0.4)",
                  borderColor: "rgba(63, 205, 199,1)",
                  borderCapStyle: 'butt',
                  borderDash: [],
                  borderDashOffset: 0.0,
                  borderJoinStyle: 'miter',
                  pointBorderColor: "rgba(63, 205, 199,1)",
                  pointBackgroundColor: "#fff",
                  pointBorderWidth: 1,
                  pointHoverRadius: 5,
                  pointHitRadius: 10,
                  responsive: true,
                  data: [65, 59, 80, 81, 56, 55, 40,19,2,34],
              }
          ]
      }
  });*/

  /*const CHART_MEMORY = document.getElementById("lineChartMemory");
  console.log(CHART_MEMORY);
  let lineChartMemory = new Chart(CHART_MEMORY,{
      type: "line",
      data: {
          labels: ["January", "February", "March", "April", "May", "June", "July"],
          datasets: [
              {
                  label: "Memory",
                  fill: false,
                  lineTension: 0.1,
                  backgroundColor: "rgba(254, 125, 125, 0.4)",
                  borderColor: "rgba(254, 125, 125, 1)",
                  borderCapStyle: 'butt',
                  borderDash: [],
                  borderDashOffset: 0.0,
                  borderJoinStyle: 'miter',
                  pointBorderColor: "rgba(254, 125, 125,1)",
                  pointBackgroundColor: "#fff",
                  pointBorderWidth: 1,
                  pointHoverRadius: 5,
                  pointHitRadius: 10,
                  responsive: true,
                  data: [65, 59, 80, 81, 56, 55, 40],
              }
          ]
      }
  });*/

  /*const CHART_NETWORK = document.getElementById("lineChartNetwork");
  console.log(CHART_NETWORK);
  let lineChart_Network = new Chart(CHART_NETWORK,{
      type: "line",
      data: {
          labels: ["January", "February", "March", "April", "May", "June", "July"],
          datasets: [
              {
                  label: "Network",
                  fill: false,
                  lineTension: 0.1,
                  backgroundColor: "rgba(112, 73, 255, 0.4)",
                  borderColor: "rgba(112, 73, 255, 1)",
                  borderCapStyle: 'butt',
                  borderDash: [],
                  borderDashOffset: 0.0,
                  borderJoinStyle: 'miter',
                  pointBorderColor: "rgba(112, 73, 255,1)",
                  pointBackgroundColor: "#fff",
                  pointBorderWidth: 1,
                  pointHoverRadius: 5,
                  pointHitRadius: 10,
                  responsive: true,
                  data: [65, 59, 80, 81, 56, 55, 40],
              }
          ]
      }
  });*/

  /*const CHART_FS = document.getElementById("lineChartFS");
  console.log(CHART_FS);
  let lineChartFS = new Chart(CHART_FS,{
      type: "line",
      data: {
          labels: ["January", "February", "March", "April", "May", "June", "July"],
          datasets: [
              {
                  label: "FS",
                  fill: false,
                  lineTension: 0.1,
                  backgroundColor: "rgba(255, 223, 41, 0.4)",
                  borderColor: "rgba(255, 223, 41, 1)",
                  borderCapStyle: 'butt',
                  borderDash: [],
                  borderDashOffset: 0.0,
                  borderJoinStyle: 'miter',
                  pointBorderColor: "rgba(255, 223, 41,1)",
                  pointBackgroundColor: "#fff",
                  pointBorderWidth: 1,
                  pointHoverRadius: 5,
                  pointHitRadius: 10,
                  responsive: true,
                  data: [65, 59, 80, 81, 56, 55, 40],
              }
          ]
      }
  });*/
</script>

</body>

</html>

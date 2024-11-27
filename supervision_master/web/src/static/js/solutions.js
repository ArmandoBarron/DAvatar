$('#myModal').on('show.bs.modal', function(ev) {
  let button = $(ev.relatedTarget) // Button that triggered the modal
  let cts = button.data('containers') // Extract info from data-* attributes
  let modal = $(this);
  let cts_html = '';
  cts.split(' ').forEach(elem => {
    cts_html += '<span class="badge badge-info m-1" style="font-size:medium">'+elem+'</span>';
  });
  modal.find('.modal-body').html(cts_html);
});

function gotoStatus(solution) {
  location.href = '/status/'+solution;
};

function getStrContainers(containers) {
  let str = '';
  Object.values(containers).forEach(c =>{
    if (c['name']){
      str += ((str == '') ? c['name'] : ' ' + c['name']);
    }else{
      if (c['service']) str += ((str == '') ? c['service'] : ' ' + c['service']);
    }
  });
  return str;
}

var update = function () {
  $.getJSON("getsolutions")
    .done(function (data, textStatus, jqXHR) {
      var output;
      var i = 1;
      $.each(data['data'], function (key, value) {
        var size = Object.keys(value['containers']).length;
        let btn_info = '<button class="btn btn-light" type="button" title="Show containers" '+
          'data-toggle="modal" data-target="#myModal" data-containers="'+getStrContainers(value['containers'])+
          '"><i class="icon ion-ios-more-outline"></i></button>'; //ion-ios-information-outline  ion-ios-keypad
        let btn_status = '<button class="btn btn-light ml-2" type="button" title="Show status"  onclick="gotoStatus(\''+value['name']+'\')"> '+
          '<i class="icon ion-ios-analytics"></i></button>'; //ion-ios-pulse-strong  ion-network
        output += '<tr>';
        output += '<th scope="row">' + i + '</th>';
        output += '<td>' + value['name'] + '</td>';
        output += '<td>' + size + '</td>';
        output += '<td>' + btn_info+btn_status + '</td>';
        output += '</tr>';
        i++;
      });
      $("#table_solutions tbody").html(output);
    })
    .fail(function (jqXHR, textStatus, errorThrow) {
      if (console && console.log) {
        console.log("Request fail: " + textStatus);
        console.log(jqXHR)
        console.log(errorThrow)
      }
    });
}

update();
// var refInterval = window.setInterval('update()', 100000000000000);
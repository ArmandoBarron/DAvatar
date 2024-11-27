var data_structure = {};
var thresholds = {};
var medians = {};
var arrows_defs = ['low', 'medium', 'high', 'unknown'];
var arrows = [];
// var containers = [];
var metric_opt = parseInt($('#metric_opt').val(), 10);

function prepareStructure(nodes, links) {
  data_structure = {"nodes": [], "links": []};
  var index = {};
  nodes.forEach(node => {
    data_structure['nodes'].push({"id": node[1]});
    index[node[0]] = node[1];
  });
  let c = 0;
  links.forEach(link => {
    data_structure['links'].push({"source": index[link[0]], "target": index[link[1]], 'status': []});
  });
}

async function getStructure(solution) {
  let oReq = new XMLHttpRequest();
  oReq.open("GET", "/getstructure/"+solution, true);
  oReq.onload = function(oEvent) {
    if (oReq.status == 200) {
      // console.log(oReq.responseText);
      let res = JSON.parse(oReq.response);
      prepareStructure(res.data.nodes, res.data.edges);
    } else {
      console.log("Error " + oReq.status);
      return {};
    }
  };
  oReq.send();
}

function prepareStatus(res) {
  let idx = res.data.status.data_status.index;
  let data_status = res.data.status.data_status.data;
  for (let i = 5; i < idx.length; i += 6) {
    // containers.push(idx[i]);
    medians[idx[i]] = data_status[i-2];
    thresholds[idx[i]] = data_status[i];
    console.log(Object.values(medians));
  }
  //
  let n = data_structure.links.length;
  console.log(Object.values(data_structure.links));
  for (let i = 0; i < n; i++) {
    const lnk = data_structure.links[i];
    console.log("hola1")
    if (medians[lnk.source] != undefined && medians[lnk.target] != undefined) {
      for (let j = 0, n = medians[lnk.source].length - 1; j < n; j++) {
        // if (thresholds[lnk.source][j] == thresholds[lnk.target][j]) {
        //   data_structure.links[i]['status'].push(thresholds[lnk.source][j]);
        // } else if (medians[lnk.source][j] < medians[lnk.target][j]) {
        //   data_structure.links[i]['status'].push(thresholds[lnk.source][j]);
        // } else {
        //   data_structure.links[i]['status'].push(thresholds[lnk.target][j]);
        // }
        console.log("hola2")
        console.log(thresholds[lnk.source][j]);
        data_structure.links[i]['status'].push(thresholds[lnk.source][j]);
      }
    } else {
      console.log('container undefined');
    }
  }
  // console.log(data_structure.links);
}

async function getStatus(solution) {
  let oReq = new XMLHttpRequest();
  oReq.open("GET", "/solutions/"+solution+"/status/10/1", true);
  oReq.onload = function(oEvent) {
    if (oReq.status == 200) {
      let res = JSON.parse(oReq.response);
      prepareStatus(res);
      console.log(Object.values(data_structure['nodes']));
      console.log(Object.values(data_structure['links'])); 
      draw_graph(data_structure['nodes'], data_structure['links']);
    } else {
      console.log("Error " + oReq.status);
    }
  };
  oReq.send();
}
  
//choose what color circle will have, depending on its thresholds
//green for low, orange for medium, and red for high
function statusColor(threshold){
  switch (threshold) {
    case "low":
      return "green";
    case "medium":
      return "orange";
    case "high":
      return "red";
    default:
      return "gray";
  }
}

function draw_graph(nodes_data, links_data) {

  //alert(nodes_data);
  //alert(links_data);

  let width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
  let height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
  width = Math.floor(width*0.8);
  height = Math.floor(height*0.5)
  var svg = d3.select("svg");
  // width = +svg.attr("width"),
  // height = +svg.attr("height");
  var radius = 15;
  // var nodes_data =  [
  //   {"name": "Travis", "sex": "M"},
  //   {"name": "Rake", "sex": "M"},
  // ]
  // var links_data = [
  //   {"source": "Travis", "target": "Rake"},
  // ]

  //set up the simulation, nodes only for now 
  var simulation = d3.forceSimulation()
    .nodes(nodes_data);
  
  // clear previous simulation
  // d3.selectAll("g > *").remove()
  d3.selectAll("g").remove()
  simulation
    .force("center_force", null)
    .force("charge_force", null)
    .force("collision_force", null)
    .force("links", null);

  //add forces
  //add a charge to each node 
  //also add a centering force
  //and link force with id accessor to use named sources and targets 
  simulation
    .force("center_force", d3.forceCenter(width / 2, height / 2))
    .force("charge_force", d3.forceManyBody().strength(-20))
    .force("collision_force", d3.forceCollide().radius(radius*2.5))
    .force("links", d3.forceLink(links_data).id(d => d.id));

  //draw circles for the nodes 
  var node = svg.append("g")
      .attr("class", "nodes")
    .selectAll("circle")
      .data(nodes_data)
    .enter().append("circle")
      .attr("r", radius)
      .attr("fill", d => statusColor(thresholds[d.id][metric_opt]));
  node.append("title").text(d => medians[d.id][metric_opt]);
  
  //draw text for the labels
  var text = svg.append("g")
      .attr("class", "labels")
    .selectAll("text")
      .data(nodes_data)
    .enter().append("text")
      .attr("dx", 12)
      .attr("dy", ".35em")
      .text(d => d.id);

  // Per-type markers, as they don't inherit styles.
  svg.append("defs").selectAll("marker")
    .data(arrows_defs) // Different link/path types can be defined here
    // .data(['end']) // Different link/path types can be defined here
    .enter().append("marker") // This section adds in the arrows
      .attr("id", d => `arrow-${d}`)
      // .attr("id", String)
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 15)
      .attr("refY", -0.5)
      .attr("markerWidth", 6)
      .attr("markerHeight", 6)
      .attr("orient", "auto")
    .append("path")
      // .attr("fill", d => statusColor(d))
      .attr("d", "M0,-5L10,0L0,5");

  // //draw lines for the links 
  // var link = svg.append("g")
  //     .attr("class", "links")
  //   .selectAll("line")
  //     .data(links_data)
  //   .enter().append("line")
  //     .attr("stroke-width", 2);
  
  // add the links and the arrows
  var path = svg.append("g")
      // .attr("class", "paths")
      .attr("fill", "none")
      .attr("stroke-width", 1.5)
    .selectAll("path")
      .data(links_data)
    .enter().append("path")
      .attr("class", "link")
      .attr("class", d => "link-" + d.status[metric_opt])
      .attr("marker-end", d => `url(${new URL(`#arrow-${d.status[metric_opt]}`, location)})`);
      // .attr("marker-end", "url(#end)");
    
  simulation.on("tick", () => {
    path
      .attr("d", function(d) {
        var dx = d.target.x - d.source.x,
            dy = d.target.y - d.source.y,
            dr = Math.sqrt(dx * dx + dy * dy);
        return "M" + 
            d.source.x + "," + d.source.y + "A" + 
            dr + "," + dr + " 0 0,1 " + 
            d.target.x + "," + d.target.y;
      });

    //update circle positions each tick of the simulation
    node
      //constrains the nodes to be within a box
      .attr("cx", d => d.x = Math.max(radius, Math.min(width - radius, d.x)) )
      .attr("cy", d => d.y = Math.max(radius, Math.min(height - radius, d.y)) );
    
    //update label positions each tick of the simulation
    text
      //constrains the text to be within a box
      .attr("x", d => d.x = 1 + Math.max(radius, Math.min(width - radius, d.x)) )
      .attr("y", d => d.y = 1 + Math.max(radius, Math.min(height - radius, d.y)) );
        
    //update link positions 
    //simply tells one end of the line to follow one node around
    //and the other end of the line to follow the other node around
    // link
    //   .attr("x1", d => d.source.x )
    //   .attr("y1", d => d.source.y )
    //   .attr("x2", d => d.target.x )
    //   .attr("y2", d => d.target.y );
  });

  // add drag functionality, d is the node 
  var drag_handler = d3.drag()
    .on("start", (d) => {
      if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    })
    .on("drag", (d) => {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
    })
    .on("end", (d) => {
      if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    });
  drag_handler(node);
}

$('#metric_opt').change(() => {
  metric_opt = parseInt($('#metric_opt').val(), 10);
  // update graph
  if (data_structure) draw_graph(data_structure['nodes'], data_structure['links']);
});

$('document').ready(() => {
  let sol = $('#solution').data('solution');
  if (sol != '') {
    getStatus(sol);
    getStructure(sol);
    // redraw graph each interval. 60000 ms = 1 minute
    window.setInterval(() => getStatus(sol), 10000);
  }
});
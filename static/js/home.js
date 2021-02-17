var svgWidth = 960;
var svgHeight = 500;

var margin = {
  top: 20,
  right: 40,
  bottom: 90,
  left: 100
};

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

var svg = d3
  .select("#svg")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight);


var myimage = svg.append("image")
    .attr('xlink:href', 'https://1000logos.net/wp-content/uploads/2020/08/Steam-Logo.png')
    .attr('width', 200)
    .attr('height', 200)

myimage  // wait 1 seconds, then slowly change the circle's properties
	.transition()
	.duration(2000)
	.delay(1000)
	.attr("x",600)
	.attr("y",150)


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
};
      
async function moveCircle() {
    await sleep(2000);

    for (i=0; i<1000; i++) {
        await sleep(2000);
        myimage
            .transition()
            .duration(2000)
            .delay(1000)
            .attr("x",Math.random()*700)
            .attr("y",Math.random()*300)
            .attr('width', Math.random()*300)
            .attr('height', Math.random()*300)
    };
};

moveCircle();
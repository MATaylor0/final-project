d3.selectAll("#prediction").on("click", predictGame);

var names = [];

d3.json("/data").then(data => {
    names = Object.keys(data[0]);

    d3.select("#gameList").selectAll("option")
        .data(names)
        .enter()
        .append("option")
        .html(d => d);
});

var arr = [];

function predictGame() {
    var game1 = d3.selectAll("#game1").property("value");
    var game2 = d3.selectAll("#game2").property("value");
    var game3 = d3.selectAll("#game3").property("value");

    arr = [game1, game2, game3];

    console.log(arr);

    predict();
};

function predict() {
    d3.json(`/prediction/${arr}`).then((data) => {
        console.log(data);

        d3.selectAll("#output").text(data);
    });
};
d3.json('/data').then((game_data, err) => {
    if (err) throw err;

    var data = [{
        type: 'bar',
        x: game_data[1],
        y: game_data[2],
        orientation: 'v',
        text: game_data[1],
        marker: {color: '#75D5FD'}
    }]

    var layout = {
        autosize: true,
        margin: {
            l: 50,
            r: 150,
            b: 200,
            t: 50
        },
        title: "Highest Concurrent Player Count",
        plot_bgcolor: 'rgba(0, 0, 0, 0)',
        paper_bgcolor: 'rgba(0, 0, 0, 0)',
        font: {
            color: '#FFD300'
        },
        yaxis: {
            gridcolor: '#FFFFFF'
        },
        xaxis: {
            tickangle: 30
        }
    }

    Plotly.newPlot("graph1", data, layout, {displayModeBar: false});

    var prices = [];
    game_data[3].forEach((x, i) => {
        prices.push(game_data[0][game_data[3][i]]['price']);
    });

    buildTable(game_data[3], game_data[4], prices);
})

d3.json('/devs').then((d, err) => {
    if (err) throw err;
    vals = d[1];
    labs = d[0];

    console.log(labs);

    var data = [{
        marker: {
            colors: ['rgb(227, 255, 75)', 'rgb(197, 255, 93)', 'rgb(156, 255, 120)', 'rgb(113, 254, 146)', 'rgb(55, 250, 172)',
                    'rgb(0, 245, 196)', 'rgb(0, 238, 217)', 'rgb(0, 231, 233)', 'rgb(0, 223, 245)', 'rgb(0, 206, 253)']
        },
        labels: labs,
        values: vals,
        textinfo: 'label+percent',
        textposition: 'outside',
        type: 'pie'
    }];

    var layout = {
        title: 'Top 10 Developers',
        paper_bgcolor: 'rgba(0, 0, 0, 0)',
        margin: {"t": 50, "b": 50, "l": 50, "r": 50},
        showlegend: false,
        font: {
            color: '#FFD300'
        }
    };

    Plotly.newPlot('graph2', data, layout, {displayModeBar: false});
});

d3.json('/reviews').then((r, err) => {
    if (err) throw err;
    var data = [{
        type: 'bar',
        x: r[1].reverse(),
        y: r[0],
        orientation: 'h',
        text: r[1],
        marker: {color: '#75D5FD'},
    }]

    var layout = {
        autosize: true,
        margin: {
            l: 250,
            r: 50,
            b: 50,
            t: 50
        },
        title: "Highest Rated Games",
        plot_bgcolor: 'rgba(0, 0, 0, 0)',
        paper_bgcolor: 'rgba(0, 0, 0, 0)',
        font: {
            color: '#FFD300'
        },
        yaxis: {
            gridcolor: '#FFFFFF'
        },
        xaxis: {
            range: [0.99 * Math.min(...r[1]), 1],
            tickangle: 30
        }
    }

    Plotly.newPlot("graph3", data, layout, {displayModeBar: false});
});

function buildTable(x, y, z) {
    var keys = x;
    var values = y;
    var a = [];

    keys.forEach(function(x, i) {
        a.push({x: values[i]});
    });
    
    d3.select("tbody").selectAll("tr")
        .data(a)
        .enter()
        .append("tr")
        .html(function(d, i) {
            return `<th scope="row">${keys[i]}</th><td>${d.x}</td><td>${z[i] / 100}</td>`
        });
};
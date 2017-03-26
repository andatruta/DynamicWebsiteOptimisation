angular.module('dashboard').controller('analyticsController', ['$scope', '$rootScope', '$http', function ($scope, $rootScope, $http) {

	var ctrl = this;

	ctrl.versions = [];

	$http({
		method: 'GET',
		url: '/getVersions'
	}).then(function successCallback(response) {
		ctrl.versions = response.data;
		// console.log(ctrl.versions);
	}, function errorCallback(response) {
		console.log(response);
	});

	// Colours
	ctrl.colours = [
		"#2ecc71",
		"#3498db",
		"#e67e22",
		"#e74c3c",
		"#1abc9c",
		"#9b59b6",
		"#34495e",
		"#16a085",
		"#d35400",
		"#f39c12",
		"#8e44ad",
		"#c0392b"
	];

	// Build Graph
	var	margin = {top: 30, right: 40, bottom: 30, left: 50},
		width = 690 - margin.left - margin.right,
		height = 270 - margin.top - margin.bottom;

	var	parseDate = d3.time.format("%Y-%m-%d").parse;

	var	x = d3.time.scale().range([0, width]);
	var	y = d3.scale.linear().range([height, 0]);

	var	xAxis = d3.svg.axis().scale(x)
		.orient("bottom").ticks(5);

	var	yAxis = d3.svg.axis().scale(y)
		.orient("left").ticks(5);

	var lines = [];
	var versions = [];


	// var tip = d3.tip()
	// 	.attr('class', 'd3-tip')
	// 	.offset([-10, 0])
	// 	.html(function(d) {
	// 		return "<strong>Version:</strong> <span style='color:red'>" + d.frequency + "</span>";
	// })
	  
	var	svg = d3.select("#graph")
		.append("svg")
			.attr("width", width + margin.left + margin.right)
			.attr("height", height + margin.top + margin.bottom)
		.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	function make_x_axis() {        
		return d3.svg.axis()
			.scale(x)
			.orient("bottom")
			.ticks(5)
	};

	// Get the data
	d3.csv("static/dashboard/data/data.csv", function(error, data) {
		versions = d3.keys(data[0]);

		data.forEach(function(d) {
			d.date = parseDate(d.date);
			for (var i = 1; i < versions.length; i++) {
				d[versions[i]] = +d[versions[i]];
			}
		});

		for (var i = 1; i < versions.length; i++) {
			var	valueline = d3.svg.line()
				.x(function(d) { return x(d.date); })
				.y(function(d) { return y(d[versions[i + 1]]); });
			lines.push(valueline);
		}

		// Scale the range of the data
		x.domain(d3.extent(data, function(d) { return d.date; }));
		// y.domain([0, d3.max(data, function(d) { return Math.max(d["version1"], d["version2"]); })]);
		y.domain([0, d3.max(data, function(d) { return 100; })]);


		for (var i = 0; i < lines.length; i++) {
			svg.append("path")		// Add the valueline path.
				.attr("class", "line")
				.style("stroke", ctrl.colours[i])
				.attr("d", lines[i](data));
		};

		svg.append("g")			// Add the X Axis
			.attr("class", "x axis")
			.attr("transform", "translate(0," + height + ")")
			.call(xAxis);

		svg.append("g")			// Add the Y Axis
			.attr("class", "y axis")
			.call(yAxis);

		svg.append("g")         
			.attr("class", "grid")
			.attr("transform", "translate(0," + height + ")")
			.call(make_x_axis()
				.tickSize(-height, 0, 0)
				.tickFormat("")
			);

		// x-axis label
		svg.append("text")
			.attr("class", "x label")
			.attr("text-anchor", "end")
			.attr("x", width / 2)
			.attr("y", height + 30)
			.text("Date");

		// y-axis label
		svg.append("text")
			.attr("class", "y label")
			.attr("text-anchor", "end")
			.attr("y", -40)
			.attr("x", -30)
			.attr("dy", ".75em")
			.attr("transform", "rotate(-90)")
			.text("Successful conversions (%)");

		// tooltips
		// svg.selectAll("path")
		// 	.on('mouseenter', tip.show)
  //     		.on('mouseleave', tip.hide);

	});

}]);

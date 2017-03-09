var casper = require('casper').create({
	// pageSettings: {
	// 	loadImages:  false
	// }
});

if (casper.cli.has(0)) {
	var layout = casper.cli.get(0);
};

if (casper.cli.has(1)) {
	var colour = casper.cli.get(1);
};

if (casper.cli.has(2)) {
	var font = casper.cli.get(2);
};

if (casper.cli.has(3)) {
	var clicks = parseInt(casper.cli.get(3));
};

if (casper.cli.has(4)) {
	var time = parseInt(casper.cli.get(4));
};

if (casper.cli.has(5)) {
	var capture = casper.cli.get(5);
};

if (casper.cli.has(6)) {
	var version = casper.cli.get(6);
};

casper.options.viewportSize = { width: 1366, height: 768 };

casper.start('http://localhost:5000/#/', function() {
	if (capture === true) {
		this.echo("capture " + capture);
		this.capture("static/dashboard/images/previews/version" + version + ".png", {
			top: 0,
			left: 0,
			width: 1366,
			height: 768
		});
	};
});

casper.then(function() {
	var i = 0;

	if (this.exists('body.' + colour) && this.exists('h3.' + font)) {

		// Generate clicks
		this.repeat(clicks, function() {
			this.click('.read-more', function() {
				this.echo("clicked");
				if (this.visible('.post-container')) {
					this.echo("post is visible");
					this.click('.back');
				} else {
					this.echo("post is not visible");
				}
			});
			i++;
		});

		// Wait time
		this.wait(time, function() {
			this.echo("waited " + time);
		});
	}
});

casper.then(function() {
	this.click('.close-x', function() {
		this.echo("clicked x");
	})
})

casper.run(function() {
	this.exit();
});
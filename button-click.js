var casper = require('casper').create({
	pageSettings: {
        loadImages:  false
    }
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

casper.start('http://localhost:5000/#!/', function() {
	// this.echo('hello');
});

casper.then(function() {
	var i = 0;

	if (this.exists('body.' + colour) && this.exists('h3.' + font)) {
        this.echo(1);
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
    }
    else {
    	this.echo(0);
    }
});

casper.run(function() {
	this.exit();
});
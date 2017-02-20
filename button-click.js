var casper = require('casper').create();

casper.start('http://localhost:5000/#!/', function() {
	this.echo('hello');
});

casper.then(function() {
	var i = 1;

	this.repeat(4, function() {
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
});

casper.run(function() {
	this.exit();
});
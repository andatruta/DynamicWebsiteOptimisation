angular.module('app').controller('indexController', ['$scope', '$rootScope', function ($scope, $rootScope) {

	var ctrl = this;
	
	ctrl.posts = [
	{
		'title' : 'Blog post #1',
		'thumbnail' : 'static/images/pic01.jpg',
		'descr': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.'
	},
	{
		'title' : 'Blog post #2',
		'thumbnail' : 'static/images/pic02.jpg',
		'descr': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.'
	},
	{
		'title' : 'Blog post #3',
		'thumbnail' : 'static/images/pic03.jpg',
		'descr': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.'
	},
	{
		'title' : 'Blog post #4',
		'thumbnail' : 'static/images/pic04.jpg',
		'descr': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.'
	},
	{
		'title' : 'Blog post #5',
		'thumbnail' : 'static/images/pic05.jpg',
		'descr': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.'
	},
	]
}]);
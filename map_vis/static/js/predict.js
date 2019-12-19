function predict(month, weekday, airport, airline, period, predict_delay) {
	var months = {'1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'Apr', '5': 'May', 
         '6': 'Jun', '7': 'Jul', '8': 'Aug', '9': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'};

    var dayOfWeek = {'1':'Monday', '2':'Tuesday', '3':'Wednesday', '4':'Thursday', '5':'Friday', '6':'Saturday', '7':'Sunday'};

	
	var text1 = "Predicted delay for your flight of airline " + airline.airline + 
	" at " + airport.airport + " airport " + " in " + months[month.month] + " on " 
	+ dayOfWeek[weekday.weekday] + 
	" and departing in " + period.period + ": "
	var text2 = predict_delay.predict_delay + " min"

	var text1n = document.createTextNode(text1);
	var text2n = document.createTextNode(text2);
	var bold = document.createElement('strong');
	bold.appendChild(text2n)

	ele1 = document.createElement('div');
	ele1.className = "row text-center"
	ele1.appendChild(text1n)
	document.getElementById('prediction').appendChild(ele1);
	ele2 = document.createElement('div');
	ele2.className = "row text-center"
	ele2.style.fontSize = "20px";
	ele2.appendChild(bold)
	document.getElementById('prediction').appendChild(ele2);
}
//auto data refresh handler (c) 2019 powerhub
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function demo() {
	while (1){
		await sleep(1000);
	}
}


self.addEventListener('message', function() {

  self.postMessage(e.data);
}, false);
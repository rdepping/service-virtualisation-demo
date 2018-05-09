# Service Virtualisation Example

Example of how to simulate a large JSON response for graphing data using [Hoverfly](https://hoverfly.io/).  
Please read and follow the [basic tutorial for hoverfly](http://hoverfly.readthedocs.io/en/latest/pages/tutorials/basic/basic.html) before following this guide.
The graphing data is based on [cytoscape.js](http://js.cytoscape.org/)  

## Generate Simulation File

Ensure that the dependencies for the python script are installed  
`pip install requirements.txt`

Generate your simulation file:
```
genDiagram.py <num type1 nodes> <num type2 nodes> <num type3 nodes> <num edges> <cluster | even>
```

Outputs:  
* `diagram.json` - the full node/edge data
* `simulationTarget.json` - data contained in a hoverfly simulation file

Passing even will ensure a random allocation of edges between type1 nodes to type2 and type3 nodes. Cluster will dumbly attempt to
allocate the edges in a more biased way, hopefully generating larger clusters
of connected entities.

## Run Simulation
Download and install [Hoverfly](https://hoverfly.io/)
Add hoverfly to your path

```
hoverctl start
hoverctl mode spy
hoverctl destination "graphdata"
hoverctl import simulationTarget.json
```

## Verify
Without an actual server running you can still verify that hoverfly is intercepting the request and returning the simulation data as follows:

`curl --proxy localhost:8500 http://localhost:80/test/endpoint/graphdata`

For a real interception test start your browser using the hoverfly proxy and navigate to the page that will make the request.  
`chromium --proxy-server="http://localhost:8500"`

On Windows there is a corporate proxy setup in place that makes the command line option a bit more complicated.  
One option is to use a browser plugin like FoxyProxy and define the hoverfly proxy as an option in the plugin.


### Notes:
When hoverfly is running then you can continually import new simulation files without restart
Watch hoverfly logs using `hoverctl logs --follow`

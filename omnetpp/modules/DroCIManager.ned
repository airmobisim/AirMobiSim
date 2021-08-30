simple DroCIManager
{
    gates:
        input in;
        output out;
}

//
// Two instances (tic and toc) of Txc1 connected both ways.
// Tic and toc will pass messages to one another.
//
network DroCIManager1
{
    submodules:
        tic: DroCIManager;
        toc: DroCIManager;
    connections:
        tic.out --> {  delay = 0ms; } --> toc.in;
        tic.in <-- {  delay = 0ms; } <-- toc.out;
}
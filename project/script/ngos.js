const ngos = [
    {
      id: 1,
      name: "NGO1",
      location: "Mumbai",
      cause: "Education"
    },
    {
      id: 2,
      name: "NGO2",
      location: "Delhi",
      cause: "Healthcare"
    },
    {
      id: 3,
      name: "NGO3",
      location: "Mumbai",
      cause: "Environment"
    },
    {
      id: 4,
      name: "NGO4",
      location: "Bangalore",
      cause: "Children's Welfare"
    },
    {
      id: 5,
      name: "NGO5",
      location: "Delhi",
      cause: "Disaster Relief"
    }
  ];
  
  function getNgosByLocation(location) {
    return ngos.filter(ngo => ngo.location === location);
  }
  
  export { ngos, getNgosByLocation };
  
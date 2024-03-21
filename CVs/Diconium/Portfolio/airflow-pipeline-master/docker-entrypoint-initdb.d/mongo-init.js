print("Started Adding the Users. (ONLY IF DB WAS NOT INITIALIZED)");
db = db.getSiblingDB("admin");
db.createUser({
  user: "mongouser",
  pwd: "mongouserpass",
  roles: [{ role: "readWrite", db: "db" }],
});
print("End Adding the User Roles.");

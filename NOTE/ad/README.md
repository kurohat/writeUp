# What is Active Directory (AD)
- Directory service developed by MS to manage Windows domain networks
- Stores infomation replated to objects such as pcs, users, printer
- Authenticaties using Kerberos ticket
  - non-Wins cal use RADIUS/LDAP to authenticate to AD

# Why AD
- most common used identity management service in the world (95%)
- Can be exploited without ever attacking patchable exploit.
  - instead we abuse features, trusts components

# Physical AD components
## Domain Controllers
- Host copy of the AD DS (domain service) directory store
- Provide authentication and authorization services
- Replicate update to other domain controller in the domain and fores
- Allow administrative access to manage user accout and network resources
  - if we can compromise this, we controlls everything
## AD DS Data store
contains the database foles and processes that store and manage directory information for users, services, and applications
- Consists of Ntds.dit file
  - contain user, group, hash password of all user in AD
  - JUICY!!!
- Stored by defualt in the %systemRoot%\NTDS folder on all domain controller
- is accessible only through the domain controller process and protocols

# Logical AD components
## AD schema
- rules book/blueprint
- contain a deffinition of every object that can be create in AD
- enforces rule regarding object creation and configuration

![type](../pics/Screenshot%202020-06-18%20at%2002.39.25.png)

## Domains
- used to group and manage objects in an organization
- an administrative boudary for applying policies to group of objects
- A replication boundary for replicating data between domain controllers
- An authentication and authorization boundary that provide a way to limit the scope of access to resoures
- something.com

# tree
- a hierarchy of domains in AD
- share a contiguous namespace with the parent domain, eg. na.somthing.com, eu.somthing.com
- parent - child
- a trusted relationship between parent - child domain

# Forest
- a collection of tree
- share common
  - schema
  - configuration partition
  - gobal catalog to enable searching
- share the enterprise Admin and schema admins groups
- Enable truts between all domain in the forest

![forest](../pics/Screenshot%202020-06-18%20at%2002.51.30.png)

## Organizational Units (OU)
- Container that can contain users, group, computers, and other OUs


## Trusts
provide a machanism for users to gain access to resources in another domain
![trust](../pics/Screenshot%202020-06-18%20at%2002.55.18.png)

## Objects
![objects](../pics/Screenshot%202020-06-18%20at%2002.56.46.png)
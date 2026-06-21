# Ecosystem & Examples

AAYU's Intent Engine is capable of scaffolding entirely different business domains dynamically. Below is a showcase of the reference enterprise applications you can build using AAYU with **zero boilerplate code**.

## Official Domains Supported

### 1. Hospital Management System
Manage `Patient`s, schedule `Appointment`s, and write `Prescription`s with strict RBAC ensuring only a `Doctor` can write medical records.
**Command**: `aayu build "Build a Hospital Management System"`

### 2. CRM (Customer Relationship Management)
Track your business pipeline seamlessly from `Lead` to `Opportunity` to `Customer`. 
**Command**: `aayu build "Build a CRM"`

### 3. Learning Management System (LMS)
Run a school or university with `Student`, `Instructor`, and `Course` entities mapping natively via Many-to-Many junctions.
**Command**: `aayu build "Build a Learning Management System"`

### 4. Police Complaint System
A high-security portal mapping `Citizen` complaints to `Officer` investigations using a rigorous State Machine workflow.
**Command**: `aayu build "Build a Police Complaint System"`

### 5. E-Commerce Platform
A robust storefront managing `Product` catalog, `Order` processing, and `Payment` states.
**Command**: `aayu build "Build an E-Commerce Platform"`

### 6. HRMS (Human Resources)
Handle internal `Employee` data, process `LeaveRequest` workflows, and manage `Payroll` securely.
**Command**: `aayu build "Build an HRMS for employee leave and payroll"`

---

## Exploring the Output

When you run any of the build commands above, you can inspect the generated `main.aayu` file and the corresponding `.html` views in your directory. 

We highly recommend exploring the `main.aayu` file to learn how AAYU natively represents complex systems. All these generated apps will instantly compile into a secure, thread-safe web server when you run:

```bash
aayu run
```

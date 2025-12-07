"""
Deadlock Detection Simulator using Banker's Algorithm
Author: OS Learning Project
Description: Simulates deadlock detection for multiple processes and resources
"""

import time

class DeadlockDetectionSimulator:
    def __init__(self):
        self.num_processes = 0
        self.num_resources = 0
        self.max_need = []      # Maximum resources each process may request
        self.allocation = []    # Resources currently allocated to each process
        self.available = []     # Available instances of each resource
        self.need = []          # Remaining resource needs for each process
        
    def print_state(self, title="System State"):
        """Print current system state in a formatted table"""
        print(f"\n{'='*60}")
        print(f"{title:^60}")
        print(f"{'='*60}")
        
        # Print available resources
        print("\n📊 Available Resources:")
        headers = [f"R{i}" for i in range(self.num_resources)]
        print("+---" * self.num_resources + "+")
        print("| " + " | ".join(headers) + " |")
        print("+---" * self.num_resources + "+")
        print("| " + " | ".join(f"{x:^3}" for x in self.available) + " |")
        print("+---" * self.num_resources + "+")
        
        # Print processes information
        print("\n📋 Process Information:")
        print("+---------+" + "---------+" * (self.num_resources * 3) + "")
        
        # Print headers
        headers = ["Process"]
        for j in range(self.num_resources):
            headers.append(f"Max R{j}")
        for j in range(self.num_resources):
            headers.append(f"Alloc R{j}")
        for j in range(self.num_resources):
            headers.append(f"Need R{j}")
        
        header_line = "|"
        for h in headers:
            header_line += f" {h:^7} |"
        print(header_line)
        print("+---------+" + "---------+" * (self.num_resources * 3) + "")
        
        # Print process data
        for i in range(self.num_processes):
            row = [f"P{i}"]
            row.extend(self.max_need[i])
            row.extend(self.allocation[i])
            row.extend(self.need[i])
            
            row_line = "|"
            for val in row:
                if isinstance(val, str):
                    row_line += f" {val:^7} |"
                else:
                    row_line += f" {val:^7} |"
            print(row_line)
        
        print("+---------+" + "---------+" * (self.num_resources * 3) + "")
    
    def initialize_system(self):
        """Initialize the system with user input"""
        print("🔧 Initializing System...")
        print("-" * 40)
        
        # Get number of processes and resources
        while True:
            try:
                self.num_processes = int(input("Enter number of processes: "))
                if self.num_processes > 0:
                    break
                print("❌ Please enter a positive number!")
            except ValueError:
                print("❌ Please enter a valid number!")
        
        while True:
            try:
                self.num_resources = int(input("Enter number of resource types: "))
                if self.num_resources > 0:
                    break
                print("❌ Please enter a positive number!")
            except ValueError:
                print("❌ Please enter a valid number!")
        
        print(f"\nEnter available resources (total instances of each resource type):")
        self.available = []
        for i in range(self.num_resources):
            while True:
                try:
                    avail = int(input(f"  Resource R{i}: "))
                    if avail >= 0:
                        self.available.append(avail)
                        break
                    print("❌ Resources cannot be negative!")
                except ValueError:
                    print("❌ Please enter a valid number!")
        
        # Initialize arrays
        self.max_need = []
        self.allocation = []
        
        print("\nEnter Maximum Need Matrix (max resources each process may need):")
        print(f"Format: Enter {self.num_resources} values separated by spaces")
        print(f"Example for {self.num_resources} resources: 7 5 3")
        
        for i in range(self.num_processes):
            while True:
                try:
                    print(f"  Process P{i}: ", end="")
                    user_input = input().strip()
                    
                    # Handle if user entered without spaces (like "753")
                    if len(user_input.replace(" ", "")) == self.num_resources and " " not in user_input:
                        # User entered like "753" instead of "7 5 3"
                        print(f"⚠️  Detected compact input. Parsing as individual digits...")
                        values = [int(digit) for digit in user_input]
                    else:
                        # Normal space-separated input
                        values = list(map(int, user_input.split()))
                    
                    if len(values) != self.num_resources:
                        print(f"❌ Need exactly {self.num_resources} values! Got {len(values)}")
                        print(f"   Enter like: {' '.join(['X']*self.num_resources)}")
                        continue
                    
                    if any(v < 0 for v in values):
                        print("❌ Values cannot be negative!")
                        continue
                    
                    self.max_need.append(values)
                    break
                except ValueError:
                    print("❌ Please enter valid numbers!")
        
        print("\nEnter Allocation Matrix (resources currently allocated):")
        print(f"Format: Enter {self.num_resources} values separated by spaces")
        
        for i in range(self.num_processes):
            while True:
                try:
                    print(f"  Process P{i}: ", end="")
                    user_input = input().strip()
                    
                    # Handle if user entered without spaces (like "010")
                    if len(user_input.replace(" ", "")) == self.num_resources and " " not in user_input:
                        # User entered like "010" instead of "0 1 0"
                        print(f"⚠️  Detected compact input. Parsing as individual digits...")
                        values = [int(digit) for digit in user_input]
                    else:
                        # Normal space-separated input
                        values = list(map(int, user_input.split()))
                    
                    if len(values) != self.num_resources:
                        print(f"❌ Need exactly {self.num_resources} values! Got {len(values)}")
                        continue
                    
                    if any(v < 0 for v in values):
                        print("❌ Values cannot be negative!")
                        continue
                    
                    # Check allocation doesn't exceed max need
                    if any(values[j] > self.max_need[i][j] for j in range(self.num_resources)):
                        print(f"❌ Allocation cannot exceed maximum need!")
                        print(f"   Maximum for P{i}: {self.max_need[i]}")
                        print(f"   You entered: {values}")
                        continue
                    
                    self.allocation.append(values)
                    break
                except ValueError:
                    print("❌ Please enter valid numbers!")
        
        # Calculate need matrix
        self.calculate_need()
        
        print(f"\n✅ System initialized with {self.num_processes} processes and {self.num_resources} resource types")
        print(f"📊 Need Matrix calculated: Need = Max - Allocation")
    
    def calculate_need(self):
        """Calculate the Need matrix: Need = Max - Allocation"""
        self.need = []
        for i in range(self.num_processes):
            need_row = []
            for j in range(self.num_resources):
                need = self.max_need[i][j] - self.allocation[i][j]
                need_row.append(need)
            self.need.append(need_row)
    
    def safety_algorithm(self):
        """
        Banker's Safety Algorithm to check if system is in safe state
        Returns: (is_safe, safe_sequence)
        """
        print("\n🔍 Running Safety Algorithm...")
        print("-" * 40)
        
        # Work = Available
        work = self.available.copy()
        finish = [False] * self.num_processes
        safe_sequence = []
        
        iteration = 1
        
        while len(safe_sequence) < self.num_processes:
            print(f"\nIteration {iteration}:")
            print(f"  Work: {work}")
            finished_procs = [f'P{i}' for i, f in enumerate(finish) if f]
            print(f"  Finished processes: {finished_procs if finished_procs else 'None'}")
            
            found = False
            for i in range(self.num_processes):
                if not finish[i]:
                    # Check if Need[i] <= Work
                    can_allocate = True
                    for j in range(self.num_resources):
                        if self.need[i][j] > work[j]:
                            can_allocate = False
                            break
                    
                    if can_allocate:
                        print(f"  ✓ Process P{i} can be allocated (Need: {self.need[i]} <= Work: {work})")
                        print(f"    Allocating resources to P{i}...")
                        
                        # Simulate process completion
                        for j in range(self.num_resources):
                            work[j] += self.allocation[i][j]
                        
                        finish[i] = True
                        safe_sequence.append(f"P{i}")
                        found = True
                        
                        print(f"    P{i} finished. Work becomes: {work}")
                        break
                    else:
                        print(f"  ✗ Process P{i} must wait (Need: {self.need[i]} > Work: {work})")
            
            if not found:
                print("\n❌ No process found that can be allocated. System is UNSAFE!")
                return False, []
            
            iteration += 1
            if iteration <= self.num_processes:  # Only pause for first few iterations
                time.sleep(1)  # Pause for visualization
        
        print(f"\n✅ System is in SAFE state!")
        print(f"📈 Safe sequence: {' → '.join(safe_sequence)}")
        return True, safe_sequence
    
    def detect_deadlock(self):
        """Main deadlock detection function"""
        print("\n" + "="*60)
        print("DEADLOCK DETECTION SIMULATION".center(60))
        print("="*60)
        
        self.print_state("Initial State")
        
        is_safe, safe_seq = self.safety_algorithm()
        
        if is_safe:
            print("\n🎉 CONCLUSION: No deadlock detected!")
            print(f"   The system is in a safe state.")
            print(f"   Processes can complete in order: {' → '.join(safe_seq)}")
        else:
            print("\n⚠️  CONCLUSION: Deadlock detected!")
            print("   The system is in an unsafe state.")
            print("   One or more processes are deadlocked.")
        
        return is_safe, safe_seq
    
    def request_resources(self, process_id, request):
        """
        Simulate a process requesting resources
        Returns: True if request can be granted safely
        """
        print(f"\n📨 Process P{process_id} requesting resources: {request}")
        
        # Check if request is valid (request <= need)
        for j in range(self.num_resources):
            if request[j] > self.need[process_id][j]:
                print(f"❌ Request exceeds maximum need! (Request: {request[j]} > Need: {self.need[process_id][j]} for R{j})")
                return False
        
        # Check if request <= available
        for j in range(self.num_resources):
            if request[j] > self.available[j]:
                print(f"❌ Not enough resources available! (Request: {request[j]} > Available: {self.available[j]} for R{j})")
                return False
        
        print("✓ Request validation passed. Temporarily allocating resources...")
        
        # Try to allocate
        temp_available = self.available.copy()
        temp_allocation = [row.copy() for row in self.allocation]
        temp_need = [row.copy() for row in self.need]
        
        # Simulate allocation
        for j in range(self.num_resources):
            temp_available[j] -= request[j]
            temp_allocation[process_id][j] += request[j]
            temp_need[process_id][j] -= request[j]
        
        # Save original state
        original_available = self.available.copy()
        original_allocation = [row.copy() for row in self.allocation]
        original_need = [row.copy() for row in self.need]
        
        # Temporarily change state
        self.available, self.allocation, self.need = temp_available, temp_allocation, temp_need
        
        self.print_state("State After Temporary Allocation")
        
        # Check if state is safe
        is_safe, _ = self.safety_algorithm()
        
        # Restore original state
        self.available, self.allocation, self.need = original_available, original_allocation, original_need
        
        if is_safe:
            print(f"\n✅ Request by P{process_id} can be GRANTED safely")
            # Actually apply the allocation
            for j in range(self.num_resources):
                self.available[j] -= request[j]
                self.allocation[process_id][j] += request[j]
                self.need[process_id][j] -= request[j]
            print("✅ Resources have been allocated!")
            return True
        else:
            print(f"\n❌ Request by P{process_id} would lead to UNSAFE state - Request DENIED")
            return False


def run_predefined_examples():
    """Run predefined examples including deadlock detection"""
    print("\n" + "="*70)
    print("PREDEFINED EXAMPLES - DEADLOCK DETECTION".center(70))
    print("="*70)
    
    while True:
        print("\n📚 Choose an example to run:")
        print("1. Example 1: System in SAFE State (No Deadlock)")
        print("2. Example 2: System in UNSAFE State (Deadlock Detected)")
        print("3. Example 3: Resource Request Simulation")
        print("4. Example 4: Classic Deadlock Scenario (Circular Wait)")
        print("5. Return to Main Menu")
        
        example_choice = input("\nEnter your choice (1-5): ").strip()
        
        if example_choice == '1':
            # Example 1: Safe State
            print("\n" + "="*60)
            print("EXAMPLE 1: System in SAFE State".center(60))
            print("="*60)
            
            simulator = DeadlockDetectionSimulator()
            simulator.num_processes = 5
            simulator.num_resources = 3
            
            # Available resources
            simulator.available = [3, 3, 2]
            
            # Maximum Need matrix
            simulator.max_need = [
                [7, 5, 3],
                [3, 2, 2],
                [9, 0, 2],
                [2, 2, 2],
                [4, 3, 3]
            ]
            
            # Allocation matrix
            simulator.allocation = [
                [0, 1, 0],
                [2, 0, 0],
                [3, 0, 2],
                [2, 1, 1],
                [0, 0, 2]
            ]
            
            simulator.calculate_need()
            simulator.detect_deadlock()
            
        elif example_choice == '2':
            # Example 2: Unsafe State (Deadlock Detected)
            print("\n" + "="*60)
            print("EXAMPLE 2: System in UNSAFE State".center(60))
            print("="*60)
            print("⚠️  This is a classic deadlock scenario!")
            print("   All processes are waiting for resources held by others")
            
            simulator = DeadlockDetectionSimulator()
            simulator.num_processes = 3
            simulator.num_resources = 3
            
            # Available resources - Very limited
            simulator.available = [0, 0, 1]
            
            # Maximum Need matrix
            simulator.max_need = [
                [2, 1, 2],
                [1, 2, 1],
                [2, 1, 2]
            ]
            
            # Allocation matrix - Circular dependency
            simulator.allocation = [
                [2, 0, 1],  # P0 holds 2 of R0, 0 of R1, 1 of R2
                [0, 1, 0],  # P1 holds 0 of R0, 1 of R1, 0 of R2
                [1, 0, 0]   # P2 holds 1 of R0, 0 of R1, 0 of R2
            ]
            
            simulator.calculate_need()
            simulator.detect_deadlock()
            
        elif example_choice == '3':
            # Example 3: Resource Request
            print("\n" + "="*60)
            print("EXAMPLE 3: Resource Request Simulation".center(60))
            print("="*60)
            
            # First create a safe system
            simulator = DeadlockDetectionSimulator()
            simulator.num_processes = 5
            simulator.num_resources = 3
            
            simulator.available = [3, 3, 2]
            simulator.max_need = [
                [7, 5, 3],
                [3, 2, 2],
                [9, 0, 2],
                [2, 2, 2],
                [4, 3, 3]
            ]
            simulator.allocation = [
                [0, 1, 0],
                [2, 0, 0],
                [3, 0, 2],
                [2, 1, 1],
                [0, 0, 2]
            ]
            
            simulator.calculate_need()
            print("\nFirst, let's check the initial state:")
            simulator.detect_deadlock()
            
            # Test different resource requests
            print("\n" + "="*60)
            print("TESTING DIFFERENT RESOURCE REQUESTS".center(60))
            print("="*60)
            
            # Test 1: Safe request
            print("\n📋 Test 1: Safe Resource Request")
            print("-" * 40)
            simulator.request_resources(process_id=1, request=[1, 0, 2])
            
            # Test 2: Unsafe request
            print("\n📋 Test 2: Unsafe Resource Request")
            print("-" * 40)
            simulator.request_resources(process_id=0, request=[7, 4, 3])
            
        elif example_choice == '4':
            # Example 4: Classic Deadlock Scenario (Circular Wait)
            print("\n" + "="*60)
            print("EXAMPLE 4: Classic Circular Wait Deadlock".center(60))
            print("="*60)
            print("💡 This demonstrates the classic dining philosophers problem")
            print("   Each process holds one resource and needs another")
            
            simulator = DeadlockDetectionSimulator()
            simulator.num_processes = 4
            simulator.num_resources = 4
            
            # Each resource has only 1 instance
            simulator.available = [0, 0, 0, 0]
            
            # Circular dependency: P0 needs R1, P1 needs R2, P2 needs R3, P3 needs R0
            simulator.max_need = [
                [0, 1, 0, 0],  # P0 needs R1
                [0, 0, 1, 0],  # P1 needs R2
                [0, 0, 0, 1],  # P2 needs R3
                [1, 0, 0, 0]   # P3 needs R0
            ]
            
            # Each holds one resource
            simulator.allocation = [
                [1, 0, 0, 0],  # P0 holds R0
                [0, 1, 0, 0],  # P1 holds R1
                [0, 0, 1, 0],  # P2 holds R2
                [0, 0, 0, 1]   # P3 holds R3
            ]
            
            simulator.calculate_need()
            print("\n🔍 Analyzing the circular wait scenario:")
            print("• P0 holds R0, needs R1")
            print("• P1 holds R1, needs R2")
            print("• P2 holds R2, needs R3")
            print("• P3 holds R3, needs R0")
            print("• This creates a circular wait → DEADLOCK!")
            
            simulator.detect_deadlock()
            
        elif example_choice == '5':
            print("↩️  Returning to main menu...")
            break
            
        else:
            print("❌ Invalid choice! Please enter 1-5.")
        
        # Ask if user wants to see another example
        if example_choice in ['1', '2', '3', '4']:
            continue_choice = input("\nWould you like to see another example? (yes/no): ").strip().lower()
            if continue_choice not in ['yes', 'y']:
                break


def interactive_mode():
    """Run interactive mode where user can configure system"""
    print("\n" + "="*60)
    print("INTERACTIVE DEADLOCK DETECTION".center(60))
    print("="*60)
    
    simulator = DeadlockDetectionSimulator()
    
    while True:
        print("\n📝 Menu:")
        print("1. Initialize new system")
        print("2. Detect deadlock")
        print("3. Make resource request")
        print("4. Show current state")
        print("5. Run predefined examples")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            simulator.initialize_system()
        elif choice == '2':
            if simulator.num_processes == 0:
                print("❌ Please initialize the system first!")
            else:
                simulator.detect_deadlock()
        elif choice == '3':
            if simulator.num_processes == 0:
                print("❌ Please initialize the system first!")
            else:
                try:
                    pid = int(input("Enter process ID: "))
                    if pid < 0 or pid >= simulator.num_processes:
                        print(f"❌ Invalid process ID! Must be between 0 and {simulator.num_processes-1}")
                        continue
                    print(f"Enter request for resources (space-separated, {simulator.num_resources} values): ")
                    req_input = input().strip()
                    
                    # Handle compact input like "100" instead of "1 0 0"
                    if len(req_input.replace(" ", "")) == simulator.num_resources and " " not in req_input:
                        req = [int(digit) for digit in req_input]
                    else:
                        req = list(map(int, req_input.split()))
                    
                    if len(req) != simulator.num_resources:
                        print(f"❌ Need exactly {simulator.num_resources} values!")
                        continue
                    simulator.request_resources(pid, req)
                except ValueError:
                    print("❌ Invalid input! Please enter numbers only.")
        elif choice == '4':
            if simulator.num_processes == 0:
                print("❌ System not initialized!")
            else:
                simulator.print_state()
        elif choice == '5':
            run_predefined_examples()
        elif choice == '6':
            print("👋 Exiting simulator. Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please enter 1-6.")


def main():
    """Main function"""
    print("🔐 DEADLOCK DETECTION SIMULATOR")
    print("📚 Implements Banker's Algorithm for Deadlock Detection")
    print("-" * 60)
    print("\nKey Concepts:")
    print("• Safe State: System can avoid deadlock")
    print("• Unsafe State: Potential for deadlock exists")
    print("• Need = Max - Allocation")
    print("• Banker's Algorithm finds safe sequence if it exists")
    print("-" * 60)
    
    while True:
        print("\nHow would you like to run the simulator?")
        print("1. Interactive Mode (Configure your own system)")
        print("2. Run Predefined Examples")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == '1':
            interactive_mode()
            break
        elif choice == '2':
            run_predefined_examples()
            
            # Ask if user wants to try interactive mode
            try_again = input("\nWould you like to try interactive mode? (yes/no): ").strip().lower()
            if try_again in ['yes', 'y']:
                interactive_mode()
            break
        elif choice == '3':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please enter 1-3.")


if __name__ == "__main__":
    main()
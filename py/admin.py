import tkinter as tk
import core

# This class is responsible for displaying the request list, and
# marking requests as played
class RequestListGUI:
    
    def __init__(self, update_interval=30000): #update every 30 seconds
        # Setup API comms, other stuff
        self.a = core.ApiComms()
        self.update_interval = update_interval
        self.requests = []   
        
        # Setup GUI
        self.root = tk.Tk()

        # Setup the listbox
        self.request_listbox = tk.Listbox(self.root, width=70, height=25) # set the size of the listbox
        self.request_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Setup the scrollbar
        self.scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.request_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.request_listbox.config(yscrollcommand=self.scrollbar.set)

        # Setup the button
        self.button = tk.Button(self.root, text="Mark as Played", command=self.mark_selected_as_played)
        self.button.pack()

        # Update the requests
        self.update_requests()
        self.update_interval = update_interval
        self.root.after(update_interval, self.update_requests)    

    def update_requests(self):
        self.requests = self.a.get_request_list() # get requests from the API
        self.request_listbox.delete(0, tk.END) # clear the listbox

        # If there are no requests, add a message to the listbox
        if not self.requests or len(self.requests) == 0:
            self.request_listbox.insert(tk.END, "No requests")
        else:
            for request in self.requests:
                request_text = request["song_title"] + " - (" + str(request["votes"]) + " vote(s))"
                self.request_listbox.insert(tk.END, request_text) # add each request to the listbox
        
        self.root.after(self.update_interval, self.update_requests) # schedule the next update
        
    def mark_selected_as_played(self):
        # Get the selected request
        request_index = self.request_listbox.curselection()
        if not request_index or len(request_index) == 0:
            return

        # Get the request
        request_index = request_index[0]
        request = self.requests[request_index]
        
        # Mark the request as played, then update the listbox
        self.a.mark_song_as_played(request["request_id"])
        self.update_requests()
        
    def start(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = RequestListGUI()
    gui.start()
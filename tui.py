from textual.app import App
from textual.widgets import Static, ProgressBar
from Bio import SeqIO

class ChunkingApp(App):
     def compose(self):
         yield Static("Genome Chunking Progress")
         yield ProgressBar()
         
         
     def on_mount(self):
         record = next(SeqIO.parse("mock_genome.fasta","fasta"))
         self.genome = str(record.seq)
         self.chunk_size = 1_000_000
         self.total_chunks = (len(self.genome) + self.chunk_size -1) // self.chunk_size
         self.current_chunk = 0
         self.chunks = []
         
         
         self.progress_bar = self.query_one(ProgressBar)
         self.progress_bar.total = self.total_chunks
         
         
         self.set_interval(0.2,self.process_next_chunk)
         
     def process_next_chunk(self):
         start = self.current_chunk * self.chunk_size
         end = start + self.chunk_size
         chunk = self.genome[start:end]
         self.chunks.append(chunk)
         self.current_chunk += 1
         self.query_one(ProgressBar).advance(1)
if __name__ == "__main__":
    ChunkingApp().run()
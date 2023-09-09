import unittest
from unittest.mock import patch, Mock
from queue import Queue
from coding import producer, consumer  

class TestWebLinkExtractor(unittest.TestCase):

    @patch('requests.get')
    def test_producer(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "<html></html>"
        
        q = Queue()
        producer("https://www.amazon.co.uk", q)
        
        self.assertFalse(q.empty())
        self.assertEqual(q.get(), "<html></html>")
    
    @patch('requests.get')
    def test_producer_unsuccessful_request(self, mock_get):
        mock_get.return_value.status_code = 404
        
        q = Queue()
        producer("https://www.nonexistentwebsite.com", q)
        
        self.assertTrue(q.empty())
        
    @patch('coding.BeautifulSoup')  
    def test_consumer(self, mock_bs):
        mock_bs.return_value.find_all.return_value = [{'href': 'https://www.links.co.uk'}]
        
        q = Queue()
        q.put('<html><body><a href="https://www.links.co.uk">Example</a></body></html>')
        
        with patch('builtins.print') as mock_print:
            consumer(q)
            mock_print.assert_called_with('Extracted links: [\'https://www.links.co.uk\']')

if __name__ == '__main__':
    unittest.main()

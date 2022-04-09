using System;
using HtmlAgilityPack;
using System.Net.Http;
using System.Threading.Tasks;
using System.Linq;
using System.Net;
using System.IO;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace ConsoleAppCrawler
{
    class Program
    {
        public static int count = 0;
        public static HashSet<string> urlset = new HashSet<string>();
        static void Main(string[] args)
        {
            WebCrawl("https://www.caticles.com/");
        }

        public static string ReadURL(string url)
        {
            HttpWebRequest myWebRequest;
            HttpWebResponse myWebResponse;
            String URL = url;

            try
            {
                myWebRequest = (HttpWebRequest)HttpWebRequest.Create(URL);
                myWebResponse = (HttpWebResponse)myWebRequest.GetResponse();

                Stream streamResponse = myWebResponse.GetResponseStream();//return the data stream from the internet

                StreamReader sreader = new StreamReader(streamResponse);//reads the data stream
                String Rstring = sreader.ReadToEnd();//reads it to the end
                streamResponse.Close();
                sreader.Close();
                myWebResponse.Close();

                return Rstring;
            }
            catch (Exception e)
            {
                return "Error";
            }
        }

        public static void WebCrawl(string urlvalue)
        {
            string Rstring = ReadURL(urlvalue);
            if (Rstring != "Error")
            {
                ISet<string> Links = GetNewLinks(Rstring);//gets the links only

                Parallel.ForEach(Links, value =>
                {
                    if (!urlset.Contains(value))
                    {
                        Console.WriteLine(value);
                        urlset.Add(value);
                        string Rsting = ReadURL(value);
                        ISet<string> FoundURLs = GetNewLinks(Rsting);

                        foreach (var val in FoundURLs)
                        {
                            Console.WriteLine("".PadLeft(2) + val);
                        }
                    }
                });
            }           
        }
        
        public static ISet<string> GetNewLinks(string content)
        {
            Regex regexLink = new Regex("(?<=<a\\s*?href=(?:'|\"))[^'\"]*?(?=(?:'|\"))");

            ISet<string> newLinks = new HashSet<string>();
            foreach (var match in regexLink.Matches(content))
            {
                if (!newLinks.Contains(match.ToString()) && match.ToString().Contains("http"))
                    newLinks.Add(match.ToString());
                if (newLinks.Count == 50)
                    break;
            }

            return newLinks;
        }
    }
}

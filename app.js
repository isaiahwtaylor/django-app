const fs = require('fs');
const parse = require('node-html-parser').parse;
const marked = require("marked");
const pretty = require('pretty')

const fileNames = []

fs.readdirSync('root/templates/root/blogs/md').forEach(file => {
  console.log(file);
  fileNames.push(file.split('.').slice(0, -1).join('.')
)});
console.log(fileNames)

for (let fileName of fileNames) {
   // read in markdown file
   // const fileName = "in"
   const md = fs.readFileSync(`root/templates/root/blogs/md/${fileName}.md`)
   const mdRoot = parse(md)

   // convert markdown to html
   const markhtml = marked(mdRoot.toString());

   // read template file and insert markhtml into div id content
   // then save file as blog + fileName
   fs.readFile('root/templates/root/blog-builder.html', 'utf8', (err,html)=>{
      if(err){
         throw err;
      }

      let root = parse(html);
      root.querySelector('#blog-container').set_content(markhtml)
      let output = pretty(root.toString())
      fs.writeFileSync(`root/templates/root/blogs/html-gen/blog-${fileName}.html`, output)
    });
}



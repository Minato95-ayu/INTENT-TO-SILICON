pub struct UiNode {
    pub tag: String,
    pub children: Vec<UiNode>,
    pub props: std::collections::HashMap<String, String>,
}

impl UiNode {
    pub fn new(tag: &str) -> Self {
        Self {
            tag: tag.to_string(),
            children: Vec::new(),
            props: std::collections::HashMap::new(),
        }
    }

    pub fn render(&self) -> String {
        let mut props_str = String::new();
        for (k, v) in &self.props {
            props_str.push_str(&format!(" {}=\"{}\"", k, v));
        }
        
        if self.children.is_empty() {
            format!("<{}{} />", self.tag, props_str)
        } else {
            let mut children_str = String::new();
            for child in &self.children {
                children_str.push_str(&child.render());
            }
            format!("<{}{}>{}</{}>", self.tag, props_str, children_str, self.tag)
        }
    }
}

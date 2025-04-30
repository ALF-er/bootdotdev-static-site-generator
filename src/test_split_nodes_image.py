import unittest

from split_nodes_image import split_nodes_image
from textnode import TextType, TextNode

class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_no_images(self):
        input_nodes = [
            TextNode("This is a paragraph with no images.", TextType.TEXT)
        ]
        result = split_nodes_image(input_nodes)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is a paragraph with no images.")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertIsNone(result[0].url)

    def test_single_image(self):
        input_nodes = [
            TextNode("Here is an image: ![Alt text](https://example.com/image.jpg)", TextType.TEXT)
        ]
        result = split_nodes_image(input_nodes)

        self.assertEqual(len(result), 2)

        # First part: text before image
        self.assertEqual(result[0].text, "Here is an image: ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertIsNone(result[0].url)

        # Second part: the image
        self.assertEqual(result[1].text, "Alt text")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "https://example.com/image.jpg")

    def test_multiple_images(self):
        input_nodes = [
            TextNode(
                "First image: ![Image 1](https://example.com/image1.jpg) and second image: ![Image 2](https://example.com/image2.jpg)",
                TextType.TEXT
            )
        ]
        result = split_nodes_image(input_nodes)

        self.assertEqual(len(result), 4)

        # First part: text before first image
        self.assertEqual(result[0].text, "First image: ")
        self.assertEqual(result[0].text_type, TextType.TEXT)

        # Second part: first image
        self.assertEqual(result[1].text, "Image 1")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "https://example.com/image1.jpg")

        # Third part: text between images
        self.assertEqual(result[2].text, " and second image: ")
        self.assertEqual(result[2].text_type, TextType.TEXT)

        # Fourth part: second image
        self.assertEqual(result[3].text, "Image 2")
        self.assertEqual(result[3].text_type, TextType.IMAGE)
        self.assertEqual(result[3].url, "https://example.com/image2.jpg")

    def test_image_at_beginning(self):
        input_nodes = [
            TextNode("![First image](https://example.com/first.jpg) followed by text", TextType.TEXT)
        ]
        result = split_nodes_image(input_nodes)

        self.assertEqual(len(result), 2)

        # Second part: the image
        self.assertEqual(result[0].text, "First image")
        self.assertEqual(result[0].text_type, TextType.IMAGE)
        self.assertEqual(result[0].url, "https://example.com/first.jpg")

        # Third part: text after image
        self.assertEqual(result[1].text, " followed by text")
        self.assertEqual(result[1].text_type, TextType.TEXT)

    def test_image_at_end(self):
        input_nodes = [
            TextNode("Text followed by ![last image](https://example.com/last.jpg)", TextType.TEXT)
        ]
        result = split_nodes_image(input_nodes)

        self.assertEqual(len(result), 2)

        # First part: text before image
        self.assertEqual(result[0].text, "Text followed by ")
        self.assertEqual(result[0].text_type, TextType.TEXT)

        # Second part: the image
        self.assertEqual(result[1].text, "last image")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "https://example.com/last.jpg")

    def test_empty_alt_text(self):
        input_nodes = [
            TextNode("Image with no alt text: ![](https://example.com/empty.jpg)", TextType.TEXT)
        ]
        result = split_nodes_image(input_nodes)

        self.assertEqual(len(result), 2)

        # First part: text before image
        self.assertEqual(result[0].text, "Image with no alt text: ")
        self.assertEqual(result[0].text_type, TextType.TEXT)

        # Second part: the image
        self.assertEqual(result[1].text, "")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "https://example.com/empty.jpg")

    def test_special_characters_in_url(self):
        input_nodes = [
            TextNode(
                "Special URL: ![Special](https://example.com/image-with_special-chars.jpg?param=value&other=123)",
                TextType.TEXT
            )
        ]
        result = split_nodes_image(input_nodes)

        self.assertEqual(len(result), 2)

        # Second part: the image
        self.assertEqual(result[1].text, "Special")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "https://example.com/image-with_special-chars.jpg?param=value&other=123")

    def test_multiple_nodes(self):
        input_nodes = [
            TextNode("First node with ![image1](https://example.com/image1.jpg)", TextType.TEXT),
            TextNode("Second node without images", TextType.BOLD),
            TextNode("Third node with ![image2](https://example.com/image2.jpg)", TextType.ITALIC)
        ]
        result = split_nodes_image(input_nodes)

        self.assertEqual(len(result), 5)

        # First node, first part
        self.assertEqual(result[0].text, "First node with ")
        self.assertEqual(result[0].text_type, TextType.TEXT)

        # First node, second part (image)
        self.assertEqual(result[1].text, "image1")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "https://example.com/image1.jpg")

        # Second node
        self.assertEqual(result[2].text, "Second node without images")
        self.assertEqual(result[2].text_type, TextType.BOLD)

        # Third node, first part
        self.assertEqual(result[3].text, "Third node with ")
        self.assertEqual(result[3].text_type, TextType.ITALIC)

        # Third node, second part (image)
        self.assertEqual(result[4].text, "image2")
        self.assertEqual(result[4].text_type, TextType.IMAGE)
        self.assertEqual(result[4].url, "https://example.com/image2.jpg")

    def test_preservation_of_text_type(self):
        input_nodes = [
            TextNode("Bold text with ![image](https://example.com/img.jpg)", TextType.BOLD)
        ]
        result = split_nodes_image(input_nodes)

        self.assertEqual(len(result), 2)

        # Text before image
        self.assertEqual(result[0].text, "Bold text with ")
        self.assertEqual(result[0].text_type, TextType.BOLD)

        # The image
        self.assertEqual(result[1].text, "image")
        self.assertEqual(result[1].text_type, TextType.IMAGE)

    def test_empty_nodes_filtered_out(self):
        input_nodes = [
            TextNode("![Image only](https://example.com/only.jpg)", TextType.TEXT)
        ]
        result = split_nodes_image(input_nodes)

        # Should only have one node (the image) since the before and after text nodes are empty
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Image only")
        self.assertEqual(result[0].text_type, TextType.IMAGE)
        self.assertEqual(result[0].url, "https://example.com/only.jpg")

    def test_non_normal_nodes_with_images(self):
        input_nodes = [
            TextNode("Code with ![image](https://example.com/code.jpg)", TextType.CODE),
            TextNode("Link with ![image](https://example.com/link.jpg)", TextType.LINK)
        ]
        result = split_nodes_image(input_nodes)

        self.assertEqual(len(result), 4)

        # First node, first part
        self.assertEqual(result[0].text, "Code with ")
        self.assertEqual(result[0].text_type, TextType.CODE)

        # First node, image
        self.assertEqual(result[1].text, "image")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "https://example.com/code.jpg")

        # Second node, first part
        self.assertEqual(result[2].text, "Link with ")
        self.assertEqual(result[2].text_type, TextType.LINK)

        # Second node, image
        self.assertEqual(result[3].text, "image")
        self.assertEqual(result[3].text_type, TextType.IMAGE)
        self.assertEqual(result[3].url, "https://example.com/link.jpg")

if __name__ == "__main__":
    unittest.main()
